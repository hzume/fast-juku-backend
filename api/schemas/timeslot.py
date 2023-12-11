from typing import Literal, Self
from pydantic import BaseModel, field_validator, model_validator
import datetime
from api.db import TimeslotModel
from api.schemas.meta import Meta
from api.schemas.person import Teacher


class TimeslotBase(BaseModel):
    school_id: str
    timeslot_type: Literal["lecture", "office_work", "other"]
    date: datetime.date
    timeslot_number: int
    start_time: datetime.datetime
    end_time: datetime.datetime

    # timeslot_type = "lecture"の場合はtimeslot_numberは1以上
    # timeslot_type = "office_work"の場合はtimeslot_numberは0
    @model_validator(mode="after")
    def timeslot_number_range(self):
        if self.timeslot_type == "lecture":
            if self.timeslot_number < 1:
                raise ValueError(f"timeslot_number must be >= 1, but {self.timeslot_number}")
        elif self.timeslot_type == "office_work":
            if self.timeslot_number != 0:
                raise ValueError(f"timeslot_number must be 0, but {self.timeslot_number}")
        return self.timeslot_number

    @property
    def record_type(self) -> str:
        return f"timeslot#{self.date}#{self.timeslot_number}"


class Timeslot(TimeslotBase):
    id: str

    @classmethod
    def create(cls, id: str, timeslot_base: TimeslotBase) -> Self:
        return cls(
            id=id,
            **timeslot_base.model_dump(),
        )
    
    def update(self, timeslot_base: TimeslotBase) -> Self:
        return self.model_copy(
            update={
                **timeslot_base.model_dump(),
            }
        )
    
    def to_model(self) -> TimeslotModel:
        start_time_text = self.start_time.strftime("%H:%M")
        end_time_text = self.end_time.strftime("%H:%M")
        return TimeslotModel(
            record_type=self.record_type,
            id=self.id,
            school_id=self.school_id,
            timestamp=datetime.datetime.now().isoformat(),

            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
            timeslot_number=self.timeslot_number,
            timeslot_type=self.timeslot_type,
            start_time=start_time_text,
            end_time=end_time_text,
        )

    @classmethod
    def from_model(cls, timeslot_model: TimeslotModel) -> Self:
        date = datetime.date(int(timeslot_model.year), int(timeslot_model.month), int(timeslot_model.day)) # type: ignore
        start_time_time = datetime.datetime.strptime(timeslot_model.start_time, "%H:%M").time()
        start_time = datetime.datetime.combine(date, start_time_time)
        end_time_time = datetime.datetime.strptime(timeslot_model.end_time, "%H:%M").time()
        end_time = datetime.datetime.combine(date, end_time_time)
        return cls(
            id=timeslot_model.id,
            school_id=timeslot_model.school_id,

            timeslot_type=timeslot_model.timeslot_type, # type: ignore
            date=date,
            timeslot_number=int(timeslot_model.timeslot_number), 
            start_time=start_time,
            end_time=end_time,
        )