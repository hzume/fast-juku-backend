from pydantic import BaseModel
import datetime
from schemas.person import Student

class Timeslot(BaseModel):
    timeslot_type: str
    date: datetime.date
    time: int
    duration: int
    
class Lecture(Timeslot):
    student: Student
    subject: str

class OfficeWork(Timeslot):
    pass