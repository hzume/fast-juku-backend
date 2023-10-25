from pydantic import BaseModel
import datetime 

from person import Teacher

class MeetingInfo(BaseModel):
    date: datetime.date
    duration: int

class Meeting(BaseModel):
    participants: list[Teacher]
    info: MeetingInfo

    