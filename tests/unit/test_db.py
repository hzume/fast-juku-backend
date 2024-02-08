from pathlib import Path
import pandas as pd
from moto import mock_dynamodb
from rich import print
import openpyxl as xl

from api import db
from api.cruds.timeslot import MonthlyAttendanceRepo
from api.myutils.const import GENSEN_PATH, CellBlock, LECTURE_TIMES_TO_NUMBER, DIGEST_SIZE
from api.schemas.person import Teacher, TeacherBase
from api.schemas.meta import Meta, MetaBase
from api.schemas.timeslot import Timeslot, UpdateAttendanceReq
from api.cruds.teacher import TeacherRepo
from api.cruds.meta import MetaRepo
from api.routers.timeslot import CreateAttendanceReq, make_timeslots_from_table


def load_meta(school_name: str) -> Meta:
    meta = MetaRepo.create(MetaBase(school_name=school_name))
    return meta

def load_teacher_info(path: Path, school_id: str) -> list[Teacher]:
    df = pd.read_csv(path)
    df = df.where(df.notna(), None)
    ret = [TeacherRepo.create(TeacherBase(school_id=school_id, **v))
           for v in df.to_dict(orient="index").values()]
    return ret

def load_timeslot(path: Path, school_id: str, year: int, month: int | None = None) -> list[Timeslot]:
    wb = xl.load_workbook(path, data_only=True)
    content = []
    for ws in wb.worksheets:
        if (month != None) & (~ws.title.startswith(f"{month}月")):
            continue
        for i in range(CellBlock.MAX_BLOCKS_ROW):
            block_row = []
            for row in ws.iter_rows(min_row=i+1, max_row=i+1+CellBlock.BLOCK_SIZE, values_only=True):
                block_row.append(row)
            content.append(block_row)
    teacher_list = TeacherRepo.list(school_id)
    monthly_attendance_list = make_timeslots_from_table(teacher_list, content, year, month)
    monthly_attendance_list = MonthlyAttendanceRepo.create_list(monthly_attendance_list)
    teacher = teacher_list[3]
    a = MonthlyAttendanceRepo.get(teacher.id, year, month)
    print(a.timeslot_list[:3], a.extra_payment)
    req = UpdateAttendanceReq(
        timeslot_list=a.timeslot_list,
        teacher=a.teacher,
        extra_payment=1000
    )
    print(UpdateAttendanceReq.model_validate(req, strict=True))
    b = a.update(req)
    print(b.timeslot_list[:3], b.extra_payment)

@mock_dynamodb
def test_db():
    setattr(db.DBModelBase.Meta, "host", "http://localhost:8000")
    db.DBModelBase.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

    meta = load_meta("test_school")
    teacher_list = load_teacher_info(Path("tests/data/講師情報.csv"), meta.school_id)
    teacher_dict = {teacher.display_name: teacher.id for teacher in teacher_list} 
    timeslot_list = load_timeslot(Path("tests/data/2022　新時間割表 10月分.xlsx"), meta.school_id, 2023, 1)

    # db.DBModelBase.delete_table()

# @mock_dynamodb
# def test():
#     setattr(db.DBModelBase.Meta, "host", "http://localhost:8000")
#     db.DBModelBase.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

#     meta = Meta.create(MetaBase(school_name="test_school"))

#     teacher = TeacherRepo.create(TeacherBase(
#         display_name="test_teacher",
#         given_name="test_given_name",
#         family_name="test_family_name",
#         school_id=meta.school_id,
#         lecture_hourly_pay=1000,
#         office_hourly_pay=800,
#         transportation_fee=100,
#         teacher_type="teacher",
#         email="yota040@gmail.com"
#     ))

#     teacher = TeacherRepo.get_from_email("yota040@gmail.com")
#     print(teacher)
