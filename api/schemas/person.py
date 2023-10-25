from pydantic import BaseModel

class Person(BaseModel):
    written_name: str
    fullname: tuple[str, str]

class Student(Person):
    instructor: Teacher

class Teacher(Person):
    hourly_pay: float
    office_work_hourly_pay: float
    students_in_charge: list[Student]
    available_subjects: list[str]
