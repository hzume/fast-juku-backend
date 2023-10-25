from pydantic import BaseModel

from person import Teacher
from timeslot import Timeslot
from meeting import Meeting

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



    