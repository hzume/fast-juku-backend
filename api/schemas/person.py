from pydantic import BaseModel

class Person(BaseModel):
    written_name: str
    fullname: tuple[str, str]

class Teacher(Person):
    hourly_pay: float
    office_work_hourly_pay: float
    students_in_charge: list[Person]
    available_subjects: list[str]

class Student(Person):
    instructor: Teacher
