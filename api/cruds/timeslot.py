import datetime
from typing import Optional
import pandas as pd
from pydantic import BaseModel, field_validator
from functools import singledispatch
from api.myutils.const import GENSEN_PATH

from api.schemas.timeslot import MonthlyAttendance, MonthlyAttendanceBeforeCalculate, UpdateAttendanceReq
from api.db import MonthlyAttendanceModel


class MonthlyAttendanceRepo:
    @classmethod
    def create(cls, monthly_attendance_before: MonthlyAttendanceBeforeCalculate) -> MonthlyAttendance:
        gensen = pd.read_csv(GENSEN_PATH)
        monthly_attendance = monthly_attendance_before.calc_salary(gensen)
        monthly_attendance.to_model().save()
        return monthly_attendance

    @classmethod
    def create_list(
        cls, monthly_attendance_before_list: list[MonthlyAttendanceBeforeCalculate]
    ) -> list[MonthlyAttendance]:
        gensen = pd.read_csv(GENSEN_PATH)
        monthly_attendance_list = [
            monthly_attendance_before.calc_salary(gensen)
            for monthly_attendance_before in monthly_attendance_before_list
        ]
        for monthly_attendance in monthly_attendance_list:
            monthly_attendance.to_model().save()
        return monthly_attendance_list

    @classmethod
    def get(cls, id: str, year: int, month: int) -> MonthlyAttendance:
        record_type = f"attendance#{year}-{month:02}"
        monthly_attendance_model = MonthlyAttendanceModel.get(record_type, id)
        return MonthlyAttendance.from_model(monthly_attendance_model)

    @classmethod
    def list_monthly(
        cls, school_id: str, year: int, month: int | None = None
    ) -> list[MonthlyAttendance]:
        if month == None:
            record_type = f"attendance#{year}"
        else:
            record_type = f"attendance#{year}-{month:02}"
        monthly_attendance_model_list = MonthlyAttendanceModel.school_id_index.query(
            school_id, MonthlyAttendanceModel.record_type == record_type
        )
        return [
            MonthlyAttendance.from_model(monthly_attendance_model)
            for monthly_attendance_model in monthly_attendance_model_list
        ]

    @classmethod
    def list_between(
        cls, school_id: str, start_year: int, start_month: int, end_year: int, end_month: int
    ) -> list[MonthlyAttendance]:
        monthly_attendance_model_list = MonthlyAttendanceModel.school_id_index.query(
            school_id,
            MonthlyAttendanceModel.record_type.between(
                f"attendance#{start_year}-{start_month:02}",
                f"attendance#{end_year}-{end_month:02}",
            ),
        )
        return [
            MonthlyAttendance.from_model(monthly_attendance_model)
            for monthly_attendance_model in monthly_attendance_model_list
        ]

    @classmethod
    def update(
        cls, id: str, year: int, month: int, req: UpdateAttendanceReq
    ) -> MonthlyAttendance:
        gensen = pd.read_csv(GENSEN_PATH)
        monthly_attendance_before = MonthlyAttendanceBeforeCalculate.from_monthly_attendance(cls.get(id, year, month))
        monthly_attendance = monthly_attendance_before.update(req).calc_salary(gensen)
        monthly_attendance.to_model().save()
        return monthly_attendance

    @classmethod
    def delete(cls, id: str, year: int, month: int) -> MonthlyAttendance:
        record_type = f"attendance#{year}-{month:02}"
        monthly_attendance_model = MonthlyAttendanceModel.get(record_type, id)
        monthly_attendance_model.delete()
        return MonthlyAttendance.from_model(monthly_attendance_model)

    @classmethod
    def delete_list(
        cls, school_id: str, year: int, month: int
    ) -> list[MonthlyAttendance]:
        monthly_attendance_list = cls.list_monthly(school_id, year, month)
        for monthly_attendance in monthly_attendance_list:
            monthly_attendance.to_model().delete()
        return monthly_attendance_list
