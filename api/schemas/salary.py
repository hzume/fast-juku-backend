from pydantic import BaseModel

from api.schemas.person import Teacher
from api.schemas.timeslot import Timeslot
from api.schemas.meeting import Meeting

class MonthlyAttend(BaseModel):
    teacher: Teacher
    timeslot_attendance: list[Timeslot]
    meeting_attendance: list[Meeting]

class MonthlySalary(BaseModel):
    teacher: Teacher
    gross_salary: int
    tax_amount: int
    net_salary: int
    transportation_expense: int
    
class AnnualSalary(BaseModel):
    teacher: Teacher
    monthly_salary_list: list[MonthlySalary]



