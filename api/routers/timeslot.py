from types import NoneType
from typing import Any
from zoneinfo import ZoneInfo
from fastapi import APIRouter
from unicodedata import normalize
import datetime
import re
from pydantic import BaseModel

from api.schemas.person import Teacher
from api.schemas.timeslot import (
    Meeting,
    MonthlyAttendance,
    Timeslot,
    UpdateAttendanceReq,
)
from api.cruds.teacher import TeacherRepo
from api.cruds.timeslot import MonthlyAttendanceRepo
from api.myutils.const import GENSEN_PATH

from api.myutils.utilfunc import (
    excel_date_to_datetime,
    str2int_timeslot_num,
    get_start_end_time,
)
from api.myutils.const import CellBlock, LECTURE_TIMES_TO_NUMBER, Payslip, PREPARE_TIME


router = APIRouter()


class CreateAttendanceReq(BaseModel):
    content: list[list[list[Any]]]
    meetings: list[Meeting]


@router.get("/salary/{id}", response_model=MonthlyAttendance)
async def get_monthly_salary(id: str, year: int, month: int):
    monthly_attendance = MonthlyAttendanceRepo.get(id, year, month)
    return monthly_attendance


@router.put("/salary/{id}", response_model=MonthlyAttendance)
async def update_monthly_salary(
    id: str, year: int, month: int, req: UpdateAttendanceReq
):
    monthly_attendance = MonthlyAttendanceRepo.update(id, year, month, req)
    return monthly_attendance


@router.get("/salary/bulk/{school_id}", response_model=list[MonthlyAttendance])
async def get_monthly_salary_list(school_id: str, year: int, month: int | None = None):
    monthly_attendance_list = MonthlyAttendanceRepo.list_monthly(school_id, year, month)
    return monthly_attendance_list


@router.get("/salary/bulk/{school_id}/between", response_model=list[MonthlyAttendance])
async def get_monthly_salary_list_between(
    school_id: str, start_year: int, start_month: int, end_year: int, end_month: int
):
    monthly_attendance_list = MonthlyAttendanceRepo.list_between(
        school_id, start_year, start_month, end_year, end_month
    )
    return monthly_attendance_list

@router.delete("/salary/bulk/{school_id}", response_model=list[MonthlyAttendance])
async def delete_monthly_salary_list(school_id: str, year: int, month: int):
    monthly_attendance_list = MonthlyAttendanceRepo.delete_list(school_id, year, month)
    return monthly_attendance_list


@router.post("/salary/bulk/{school_id}", response_model=list[MonthlyAttendance])
async def create_timeslots_from_class_sheet(
    school_id: str, timetable_data: CreateAttendanceReq, year: int, month: int
):
    teacher_list = TeacherRepo.list(school_id)
    id2display_name = {teacher.id: teacher.display_name for teacher in teacher_list}
    display_name2teacher = {teacher.display_name: teacher for teacher in teacher_list}

    display_name2timeslot_list = make_timeslots_from_table(
        teacher_list,
        timetable_data.content,
        year,
        month,
    )

    for meeting in timetable_data.meetings:
        for teacher_id, timeslot in meeting.make_timeslots():
            display_name = id2display_name[teacher_id]
            display_name2timeslot_list[display_name].append(timeslot)

    monthly_attendance_list = []
    for display_name, timeslot_list in display_name2timeslot_list.items():
        teacher = display_name2teacher[display_name]
        monthly_attendance = MonthlyAttendanceRepo.create(
            MonthlyAttendance(
                year=year,
                month=month,
                teacher=teacher,
                timeslot_list=timeslot_list
            )
        )
        monthly_attendance_list.append(monthly_attendance)

    return monthly_attendance_list


def make_timeslots_from_table(
    teacher_list: list[Teacher],
    content: list[list[list[Any]]],
    year: int,
    month: int,
) -> dict[str, list[Timeslot]]:

    display_name_list = [teacher.display_name for teacher in teacher_list]
    display_name2timeslot_list: dict[str, list[Timeslot]] = {
        display_name: [] for display_name in display_name_list
    }

    date = None
    for block_row in content:
        date_cell: datetime.date | int | None = block_row[CellBlock.INFO_DATE_IDX][
            CellBlock.INFO_COL
        ]
        timeslot_num_cell: str | int | None = block_row[CellBlock.INFO_TIMESLOTNUM_IDX][
            CellBlock.INFO_COL
        ]
        time_cell: str | None = block_row[CellBlock.INFO_TIME_IDX][CellBlock.INFO_COL]

        if type(date_cell) not in [datetime.date, int, NoneType]:
            continue

        if type(timeslot_num_cell) not in [str, int, NoneType]:
            raise Exception(f"timeslot_num_cell type is {type(timeslot_num_cell)}")

        if type(time_cell) not in [str, NoneType]:
            raise Exception(f"time_cell type is {type(time_cell)}")

        if (timeslot_num_cell == None) | (time_cell == None):
            continue

        # 日付を更新
        if date_cell != None:
            date = normalize_date(date_cell)  # type: ignore

        match date:
            # 更新後の日付がNoneの場合はスキップ
            case None:
                continue
            case datetime.date:
                if (date.year != year) | (date.month != month):
                    continue

        timeslot_num = get_timeslot_num(time_cell)  # type: ignore
        start_time, end_time = normalize_time(date, time_cell)  # type: ignore

        # timeslot_baseを作成
        timeslot_lecture = Timeslot(
            day=date.day,  # type: ignore
            timeslot_number=timeslot_num,
            timeslot_type="lecture",
            start_time=start_time,
            end_time=end_time,
        )

        for j in range(CellBlock.INFO_COL + 1, len(block_row[0])):
            display_name: str | None = block_row[CellBlock.BLOCK_NAME_IDX][j]

            cell1: str | None = block_row[CellBlock.BLOCK_CELL1_IDX][j]

            cell2: str | None = block_row[CellBlock.BLOCK_CELL2_IDX][j]

            if type(display_name) not in [str, NoneType]:
                raise Exception(f"display_name type is {type(display_name)}")

            if type(cell1) not in [str, NoneType]:
                raise Exception(f"cell1 type is {type(cell1)}")

            if type(cell2) not in [str, NoneType]:
                raise Exception(f"cell2 type is {type(cell2)}")

            # 講師名がNoneであれば無視
            if display_name == None:
                continue

            # cellが二つともNoneであれば無視
            if (cell1 == None) and (cell2 == None):
                continue

            # 講師名がteacher_dictになければ無視
            if display_name not in display_name_list:
                continue

            officework_end_time = get_officework_end_time(
                start_time, end_time, cell1, cell2
            )
            if officework_end_time != None:
                timeslot_office = Timeslot(
                    day=date.day,  # type: ignore
                    timeslot_number=0,
                    timeslot_type="office_work",
                    start_time=start_time,
                    end_time=officework_end_time,  # type: ignore
                )
                display_name2timeslot_list[display_name].append(timeslot_office)
            else:
                display_name2timeslot_list[display_name].append(timeslot_lecture)
    return display_name2timeslot_list


def normalize_timeslot_num(timeslot_num_cell: str | int) -> int:
    if type(timeslot_num_cell) == str:
        return str2int_timeslot_num(timeslot_num_cell)
    elif type(timeslot_num_cell) == int:
        return timeslot_num_cell
    else:
        raise Exception(f"timeslot_num_cell type is {type(timeslot_num_cell)}")


def get_timeslot_num(time_cell: str) -> int:
    time_cell = normalize("NFKC", time_cell)
    return LECTURE_TIMES_TO_NUMBER[time_cell]


def normalize_time(
    date: datetime.date, time_cell: str
) -> tuple[datetime.datetime, datetime.datetime]:
    time_cell = normalize("NFKC", time_cell)
    start_time_str, end_time_str = time_cell.split("-")
    start_time_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
    end_time_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
    start_time = datetime.datetime.combine(date, start_time_time)
    end_time = datetime.datetime.combine(date, end_time_time)
    return start_time, end_time


def normalize_date(date_cell: datetime.date | int) -> datetime.date:
    if type(date_cell) == datetime.date:
        return date_cell
    elif type(date_cell) == int:
        return excel_date_to_datetime(date_cell)
    else:
        raise Exception(f"date_cell type is {type(date_cell)}")


# cell1, cell2のどちらかが"事務"を含む場合、その時間を分単位で返す
def get_officework_end_time(
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    cell1: str | None,
    cell2: str | None,
) -> datetime.datetime | None:
    def is_officework_cell(cell: str | None) -> datetime.datetime | None:
        if cell == None:
            return None
        cell = normalize("NFKC", cell)  # type: ignore
        # cellが"事務"を含む場合
        if "事務" in cell:
            result = re.findall(r"事務(\d+)", cell)
            if len(result) == 0:
                return end_time
            else:
                td = int(result[0])
                return start_time + datetime.timedelta(minutes=td)
        else:
            return None

    cell1_officework_time = is_officework_cell(cell1)
    cell2_officework_time = is_officework_cell(cell2)

    if cell1_officework_time != None:
        return cell1_officework_time
    else:
        return cell2_officework_time
