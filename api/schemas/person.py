from typing import Self
import uuid
from pydantic import BaseModel

from api.db import TeacherModel

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


class Teacher(TeacherBase):
    id: str

    def get_base(self) -> TeacherBase:
        return TeacherBase(
            display_name=self.display_name,
            given_name=self.given_name,
            family_name=self.family_name,
            school_id=self.school_id,
            lecture_hourly_pay=self.lecture_hourly_pay,
            office_hourly_pay=self.office_hourly_pay
        )
    
    @classmethod
    def create(cls, teacher_base: TeacherBase) -> Self:
        id = uuid.uuid4().hex
        teacher = Teacher(id=id, **teacher_base.model_dump())
        return teacher
    
    def update(self, teacher_base: TeacherBase) -> Self:
        return Teacher(id=self.id, **teacher_base.model_dump())
    
    def to_model(self) -> TeacherModel:
        return TeacherModel(
            record_type="teacher",
            **self.model_dump()
        )
    
    @classmethod
    def from_model(cls, teacher_model: TeacherModel) -> Self:
        return Teacher(
            id=teacher_model.id,
            display_name=teacher_model.display_name,
            given_name=teacher_model.given_name,
            family_name=teacher_model.family_name,
            school_id=teacher_model.school_id,
            lecture_hourly_pay=teacher_model.lecture_hourly_pay,
            office_hourly_pay=teacher_model.office_hourly_pay
        )


class StudentBase(PersonBase):
    instructor_id: str

class Student(StudentBase):
    id: str
