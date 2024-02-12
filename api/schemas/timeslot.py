from typing import Any, List, Literal, Self
import numpy as np
import pandas as pd
from pydantic import BaseModel, field_validator, model_validator
import datetime
from zoneinfo import ZoneInfo
from api.db import MonthlyAttendanceModel, TimeslotMap
from api.schemas.meta import Meta
from api.schemas.person import Teacher
from api.myutils.utilfunc import time_str_2_datetime
from api.myutils.const import PREPARE_TIME, NUMBER_TO_LECTURE_TIMES


class TimeslotJS(BaseModel):
    year: int
    month: int
    day: int
    timeslot_number: int
    timeslot_type: Literal["lecture", "office_work", "other"]

    def to_timeslot(self) -> "Timeslot":
        date = datetime.date(self.year, self.month, self.day)
        time_str = NUMBER_TO_LECTURE_TIMES[self.timeslot_number]
        start_time_str, end_time_str = time_str.split("-")
        start_time_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        end_time_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
        start_time = datetime.datetime.combine(date, start_time_time)
        end_time = datetime.datetime.combine(date, end_time_time)
        return Timeslot(
            day=self.day,
            start_time=start_time,
            end_time=end_time,
            timeslot_number=self.timeslot_number,
            timeslot_type=self.timeslot_type
        )


class Timeslot(BaseModel):
    day:int
    start_time: datetime.datetime
    end_time: datetime.datetime
    timeslot_number: int
    timeslot_type: Literal["lecture", "office_work", "other"]

    @model_validator(mode="after")
    def timeslot_number_range(self) -> Self:
        if self.timeslot_type == "lecture":
            if self.timeslot_number < 1:
                raise ValueError(f"timeslot_number must be >= 1, but {self.timeslot_number}")
        elif self.timeslot_type == "office_work":
            if self.timeslot_number != 0:
                raise ValueError(f"timeslot_number must be 0, but {self.timeslot_number}")
        return self
    
    @property
    def start_time_str(self) -> str:
        return self.start_time.strftime("%H:%M")
    
    @property
    def end_time_str(self) -> str:
        return self.end_time.strftime("%H:%M")


class UpdateAttendanceReq(BaseModel):
    timeslot_js_list: list[TimeslotJS]
    extra_payment: int
    remark: str
    teacher: Teacher


class MonthlyAttendanceBeforeCalculate(BaseModel):
    year: int
    month: int
    teacher: Teacher
    timeslot_list: list[Timeslot]
    extra_payment: int = 0
    remark: str = ""

    @field_validator("month")
    @classmethod
    def month_range(cls, v):
        if v < 1 or v > 12:
            raise ValueError(f"month must be in range 1-12, but {v}")
        return v
    
    @field_validator("year")
    @classmethod
    def year_range(cls, v):
        if v < 1000 or v > 9999:
            raise ValueError(f"year must be in range 1000-9999, but {v}")
        return v
    
    def update(self, req: UpdateAttendanceReq) -> "MonthlyAttendanceBeforeCalculate":
        time_slot_list = [timeslot_js.to_timeslot() for timeslot_js in req.timeslot_js_list]
        return MonthlyAttendanceBeforeCalculate(
            year=self.year,
            month=self.month,
            teacher=req.teacher,
            timeslot_list=time_slot_list,
            extra_payment=req.extra_payment,
            remark=req.remark,
        )
    
    @classmethod
    def from_monthly_attendance(cls, monthly_attendance: "MonthlyAttendance") -> "MonthlyAttendanceBeforeCalculate":
        return MonthlyAttendanceBeforeCalculate(
            year=monthly_attendance.year,
            month=monthly_attendance.month,
            teacher=monthly_attendance.teacher,

            timeslot_list=monthly_attendance.timeslot_list,
            extra_payment=monthly_attendance.extra_payment,
            remark=monthly_attendance.remark
        )
    
    def calc_salary(self, gensen: pd.DataFrame) -> "MonthlyAttendance":
        teacher = self.teacher
        timeslot_list = self.timeslot_list
        year = self.year
        month = self.month

        monthly_lectures: list[list[Timeslot]] = [[] for _ in range(31)]
        monthly_officeworks: list[list[Timeslot]] = [[] for _ in range(31)]
        for timeslot in timeslot_list:
            if timeslot.timeslot_type == "lecture":
                monthly_lectures[timeslot.day-1].append(timeslot)
            elif timeslot.timeslot_type == "office_work":
                monthly_officeworks[timeslot.day-1].append(timeslot)
            else:
                raise ValueError(f"timeslot_type must be lecture or office_work, but {timeslot.timeslot_type}")
        

        daily_lecture_amount = [0] * 31
        daily_officework_amount = [0] * 31
        daily_latenight_amount = [0] * 31
        daily_over_eight_hour_amount = [0] * 31
        daily_attendance = np.zeros(31)
        daily_salary = np.zeros(31)
        for day in range(31):
            # 単位は時間[hour]
            daily_lectures = monthly_lectures[day]
            daily_officeworks = monthly_officeworks[day]

            if len(daily_lectures)+len(daily_officeworks) == 0:
                continue

            lecture_amount_min = sum(
                [
                    int((timeslot.end_time - timeslot.start_time).seconds / 60)
                    for timeslot in daily_lectures
                ]
            )
            officework_amount_min = sum(
                [
                    int((timeslot.end_time - timeslot.start_time).seconds / 60)
                    for timeslot in daily_officeworks
                ]
            )

            # 準備時間
            if len(daily_lectures) == 0:
                prepare_amount_min_before_end = 0
                prepare_amount_min_after_end = 0
            else:
                prepare_amount_min_after_end = (
                    len(daily_lectures) + 1
                ) * PREPARE_TIME
                prepare_amount_min_before_end = (
                    len(daily_lectures) - 1
                ) * PREPARE_TIME
            officework_amount_min += prepare_amount_min_after_end + prepare_amount_min_before_end

            daily_salary_day = (
                teacher.lecture_hourly_pay * lecture_amount_min / 60
                + teacher.office_hourly_pay * officework_amount_min / 60
            )

            # 深夜勤務手当
            end_time = max(
                [timeslot.end_time for timeslot in daily_lectures]
                + [timeslot.end_time for timeslot in daily_officeworks]
            ) + datetime.timedelta(minutes=prepare_amount_min_after_end)
            if end_time.hour < 12:
                latenight_boundary = datetime.datetime.combine(
                    datetime.date(year, month, day + 1), datetime.time(10)
                )
            else:
                latenight_boundary = datetime.datetime.combine(
                    datetime.date(year, month, day + 1), datetime.time(22)
                )
            if (end_time > latenight_boundary):
                latenight_amount_min = int((end_time - latenight_boundary).seconds / 60)
            else:
                latenight_amount_min = 0
            daily_salary_day += (
                0.25 * teacher.office_hourly_pay * latenight_amount_min / 60
            )

            # 8時間超勤務手当
            over_eight_hour_amount_min = max(0, lecture_amount_min + officework_amount_min - 8 * 60)
            daily_salary_day += (
                0.25 * teacher.office_hourly_pay * over_eight_hour_amount_min / 60
            )


            daily_salary[day] = daily_salary_day

            daily_lecture_amount[day] = lecture_amount_min
            daily_officework_amount[day] = officework_amount_min
            daily_latenight_amount[day] = latenight_amount_min
            daily_over_eight_hour_amount[day] = over_eight_hour_amount_min
            daily_attendance[day] = (len(daily_lectures)+len(daily_officeworks) > 0)

        monthly_gross_amount: float = np.sum(daily_salary) + teacher.fixed_salary # type: ignore
        monthly_trans_fee: float = np.sum(daily_attendance) * teacher.trans_fee # type: ignore
                
        monthly_gross_extra = monthly_gross_amount + self.extra_payment
        idx = (gensen["min"] <= monthly_gross_extra) & (monthly_gross_extra < gensen["max"])
        assert np.sum(idx) == 1
        v: float = gensen[idx]["-1"].values[0]
        if v < 1:
            monthly_tax_amount = v * monthly_gross_extra
        else:
            monthly_tax_amount = v

        return MonthlyAttendance(
            year=self.year,
            month=self.month,
            teacher=self.teacher,
            timeslot_list=timeslot_list,

            daily_lecture_amount=daily_lecture_amount,
            daily_officework_amount=daily_officework_amount,
            daily_latenight_amount=daily_latenight_amount,
            daily_over_eight_hour_amount=daily_over_eight_hour_amount,
            daily_attendance=daily_attendance.astype(bool).tolist(),

            monthly_gross_salary = int(monthly_gross_amount),
            monthly_tax_amount = int(monthly_tax_amount),
            monthly_trans_fee = int(monthly_trans_fee),
            extra_payment=self.extra_payment,
            remark=self.remark,
        )


class MonthlyAttendance(MonthlyAttendanceBeforeCalculate):
    daily_lecture_amount: list[int] = [0]*31
    daily_officework_amount: list[int] = [0]*31
    daily_latenight_amount: list[int] = [0]*31
    daily_over_eight_hour_amount: list[int] = [0]*31
    daily_attendance: list[bool] = [False]*31

    monthly_gross_salary: int = 0
    monthly_tax_amount: int = 0
    monthly_trans_fee: int = 0

    @property
    def record_type(self) -> str:
        return f"attendance#{self.year}-{self.month:02}"

    def to_model(self) -> MonthlyAttendanceModel:
        timeslot_list = [TimeslotMap(
            day=timeslot.day,
            start_time=timeslot.start_time_str,
            end_time=timeslot.end_time_str,
            timeslot_number=timeslot.timeslot_number,
            timeslot_type=timeslot.timeslot_type,
        ) for timeslot in self.timeslot_list]
        
        return MonthlyAttendanceModel(
            record_type=self.record_type,
            timestamp=datetime.datetime.now().isoformat(),
            year=self.year,
            month=self.month,
            timeslot_list=timeslot_list,

            daily_lecture_amount=self.daily_lecture_amount,
            daily_office_amount=self.daily_officework_amount,
            daily_latenight_amount=self.daily_latenight_amount,
            daily_over_eight_hour_amount=self.daily_over_eight_hour_amount,
            daily_attendance=self.daily_attendance,

            monthly_gross_salary=self.monthly_gross_salary,
            monthly_tax_amount=self.monthly_tax_amount,
            monthly_trans_fee=self.monthly_trans_fee,
            extra_payment=self.extra_payment,
            remark=self.remark,

            **self.teacher.model_dump(),
        )
    
    @classmethod
    def from_model(cls, monthly_attendance_model: MonthlyAttendanceModel) -> "MonthlyAttendance":
        year = int(monthly_attendance_model.year)
        month = int(monthly_attendance_model.month)
        timeslot_list = [Timeslot(
            day=int(timeslot.day),
            start_time=time_str_2_datetime(year, month, int(timeslot.day), timeslot.start_time),
            end_time=time_str_2_datetime(year, month, int(timeslot.day), timeslot.end_time),
            timeslot_number=int(timeslot.timeslot_number),
            timeslot_type=timeslot.timeslot_type, # type: ignore
        ) for timeslot in monthly_attendance_model.timeslot_list]

        if monthly_attendance_model.remark == None:
            monthly_attendance_model.remark = ""

        return MonthlyAttendance(
            year=year,
            month=month,

            daily_lecture_amount=monthly_attendance_model.daily_lecture_amount, # type: ignore
            daily_officework_amount=monthly_attendance_model.daily_office_amount, # type: ignore
            daily_latenight_amount=monthly_attendance_model.daily_latenight_amount, # type: ignore
            daily_over_eight_hour_amount=monthly_attendance_model.daily_over_eight_hour_amount, # type: ignore
            daily_attendance=monthly_attendance_model.daily_attendance, # type: ignore

            monthly_gross_salary=int(monthly_attendance_model.monthly_gross_salary),
            monthly_tax_amount=int(monthly_attendance_model.monthly_tax_amount),
            monthly_trans_fee=int(monthly_attendance_model.monthly_trans_fee),
            extra_payment=int(monthly_attendance_model.extra_payment),
            remark=monthly_attendance_model.remark,

            teacher=Teacher.from_model_monthly(monthly_attendance_model),
            timeslot_list=timeslot_list,
        )
    

class Meeting(BaseModel):
    year: int
    month: int
    day: int
    start_time: str
    end_time: str
    teacher_ids: list[str]

    def make_timeslots(self) -> list[tuple[str, Timeslot]]:
        date = datetime.date(self.year, self.month, self.day)
        start_time_time = datetime.datetime.strptime(self.start_time, "%H:%M").time()
        start_time = datetime.datetime.combine(date, start_time_time)
        end_time_time = datetime.datetime.strptime(self.end_time, "%H:%M").time()
        end_time = datetime.datetime.combine(date, end_time_time)
        timeslot = Timeslot(
            timeslot_type="office_work",
            day=self.day,
            timeslot_number=0,
            start_time=start_time,
            end_time=end_time,
        )
        return [(teacher_id, timeslot) for teacher_id in self.teacher_ids]