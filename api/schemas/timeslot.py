from pydantic import BaseModel
import datetime
from person import Student

class Lecture(BaseModel):
    student: Student
    subject: str

class Timeslot(BaseModel):
    timeslot_type: str
    date: datetime.date
    time: int
    

