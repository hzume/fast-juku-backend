import datetime
from typing import Literal, Self
from hashlib import shake_128
from pydantic import BaseModel, model_validator

from api.db import MonthlyAttendanceModel, TeacherModel
from api.myutils.utilfunc import YearMonth
from api.myutils.const import DIGEST_SIZE


class PersonBase(BaseModel):
    display_name: str
    given_name: str
    family_name: str
    school_id: str


class Person(PersonBase):
    id: str


class TeacherBase(PersonBase):
    lecture_hourly_pay: float
    office_hourly_pay: float
    trans_fee: float = 0.0
    teacher_type: Literal["teacher"]
    sub: str | None = None


class Teacher(TeacherBase):
    id: str

    def get_base(self) -> TeacherBase:
        return TeacherBase(
            display_name=self.display_name,
            given_name=self.given_name,
            family_name=self.family_name,
            school_id=self.school_id,
            lecture_hourly_pay=self.lecture_hourly_pay,
            office_hourly_pay=self.office_hourly_pay,
            trans_fee=self.trans_fee,
            teacher_type=self.teacher_type,
            sub=self.sub,
        )

    @classmethod
    def create(cls, teacher_base: TeacherBase) -> "Teacher":
        shake = shake_128()
        shake.update(teacher_base.display_name.encode("utf-8"))
        shake.update(teacher_base.school_id.encode("utf-8"))
        id = shake.hexdigest(DIGEST_SIZE)

        teacher = Teacher(id=id, **teacher_base.model_dump())
        return teacher

    def update(self, teacher_base: TeacherBase) -> "Teacher":
        return Teacher(id=self.id, **teacher_base.model_dump())

    def to_model(self) -> TeacherModel:
        return TeacherModel(
            record_type="teacher",
            timestamp=datetime.datetime.now().isoformat(),
            **self.model_dump(),
        )

    @classmethod
    def from_model(cls, teacher_model: TeacherModel) -> "Teacher":
        return Teacher(
            id=teacher_model.id,
            display_name=teacher_model.display_name,
            given_name=teacher_model.given_name,
            family_name=teacher_model.family_name,
            school_id=teacher_model.school_id,
            lecture_hourly_pay=teacher_model.lecture_hourly_pay,
            office_hourly_pay=teacher_model.office_hourly_pay,
            trans_fee=teacher_model.trans_fee,
            teacher_type=teacher_model.teacher_type,  # type: ignore
            sub=teacher_model.sub,
        )
    
    @classmethod
    def from_model_monthly(cls, monthly_timeslot_list: MonthlyAttendanceModel) -> "Teacher":
        return Teacher(
            id=monthly_timeslot_list.id,
            display_name=monthly_timeslot_list.display_name,
            given_name=monthly_timeslot_list.given_name,
            family_name=monthly_timeslot_list.family_name,
            school_id=monthly_timeslot_list.school_id,
            lecture_hourly_pay=monthly_timeslot_list.lecture_hourly_pay,
            office_hourly_pay=monthly_timeslot_list.office_hourly_pay,
            trans_fee=monthly_timeslot_list.trans_fee,
            teacher_type=monthly_timeslot_list.teacher_type,  # type: ignore
            sub=monthly_timeslot_list.sub,
        )
