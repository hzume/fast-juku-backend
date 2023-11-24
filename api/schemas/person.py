from pydantic import BaseModel

class PersonBase(BaseModel):
    display_name: str
    given_name: str
    family_name: str
    school_name: str

class Person(PersonBase):
    id: str

class TeacherBase(PersonBase):
    class_hourly_pay: float
    office_hourly_pay: float
    available_subjects: set[str]

class Teacher(TeacherBase):
    id: str

class StudentBase(PersonBase):
    instructor_id: str

class Student(StudentBase):
    id: str
