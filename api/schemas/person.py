import datetime
from typing import Literal, Self
import uuid
from pydantic import BaseModel, model_validator

from api.db import TeacherModel
from api.myutils.utilfunc import YearMonth

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


class Teacher(TeacherBase):
    id: str
    year: int | None = None
    month: int | None = None

    @model_validator(mode="after")
    def check_year_month(self):
        if (self.year == None) & (self.month != None):
            raise ValueError("year must be specified if month is specified")
        elif (self.year != None) & (self.month == None):
            raise ValueError("month must be specified if year is specified")
        return self

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
        )
    
    @classmethod
    def create(cls, teacher_base: TeacherBase) -> "Teacher":
        id = uuid.uuid4().hex
        teacher = Teacher(id=id, **teacher_base.model_dump())
        return teacher
    
    def update(self, teacher_base: TeacherBase, year_month: YearMonth | None = None) -> "Teacher":
        match year_month:
            case YearMonth():
                return Teacher(id=self.id, year=year_month.year, month=year_month.month, **teacher_base.model_dump())
            case None:
                return Teacher(id=self.id, **teacher_base.model_dump())
    
    def to_model(self) -> TeacherModel:
        match self.year:
            case int():
                return TeacherModel(
                    record_type=f"teacher#{self.year}-{self.month}",
                    timestamp=datetime.datetime.now().isoformat(),
                    **self.model_dump()
                )
            case None:
                return TeacherModel(
                    record_type="teacher",
                    timestamp=datetime.datetime.now().isoformat(),
                    **self.model_dump()
                )
    
    @classmethod
    def from_model(cls, teacher_model: TeacherModel) -> "Teacher":
        match teacher_model.year:
            case float():
                year = int(teacher_model.year)
            case None:
                year = None

        match teacher_model.month:
            case float():
                month = int(teacher_model.month)
            case None:
                month = None

        return Teacher(
            id=teacher_model.id,
            display_name=teacher_model.display_name,
            given_name=teacher_model.given_name,
            family_name=teacher_model.family_name,
            school_id=teacher_model.school_id,
            lecture_hourly_pay=teacher_model.lecture_hourly_pay,
            office_hourly_pay=teacher_model.office_hourly_pay,
            trans_fee=teacher_model.trans_fee,
            teacher_type=teacher_model.teacher_type, # type: ignore
            year=year,
            month=month,
        )
