from typing import Literal, Self
from pydantic import BaseModel, field_validator, model_validator
import datetime
from api.db import TimeslotModel
from api.schemas.meta import Meta
from schemas.person import Student, Teacher


class TimeslotBase(BaseModel):
    id: str
    school_id: str
    timeslot_type: Literal["lecture", "office_work", "other"]
    date: datetime.date
    timeslot_number: int

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
    display_name: str
    given_name: str
    family_name: str
    lecture_hourly_pay: float
    office_hourly_pay: float

    start_time: datetime.time
    end_time: datetime.time

    @classmethod
    def create(
            cls, 
            timeslot_base: TimeslotBase, 
            meta: Meta, 
            teacher: Teacher
        ) -> Self:

        start_time = meta.start_time(timeslot_base.timeslot_number)
        end_time = meta.end_time(timeslot_base.timeslot_number)
        return Timeslot(
            id=timeslot_base.id,
            school_id=timeslot_base.school_id,
            timeslot_type=timeslot_base.timeslot_type,
            date=timeslot_base.date,
            timeslot_number=timeslot_base.timeslot_number,

            display_name=teacher.display_name,
            given_name=teacher.given_name,
            family_name=teacher.family_name,
            lecture_hourly_pay=teacher.lecture_hourly_pay,
            office_hourly_pay=teacher.office_hourly_pay,

            start_time=start_time,
            end_time=end_time
        )
    
    def update(
            self,
            timeslot_base: TimeslotBase,
            meta: Meta,
            teacher: Teacher
        ) -> Self:

        start_time = meta.start_time(timeslot_base.timeslot_number)
        end_time = meta.end_time(timeslot_base.timeslot_number)
        return Timeslot(
            id=timeslot_base.id,
            school_id=timeslot_base.school_id,
            timeslot_type=timeslot_base.timeslot_type,
            date=timeslot_base.date,
            timeslot_number=timeslot_base.timeslot_number,

            display_name=teacher.display_name,
            given_name=teacher.given_name,
            family_name=teacher.family_name,
            lecture_hourly_pay=teacher.lecture_hourly_pay,
            office_hourly_pay=teacher.office_hourly_pay,

            start_time=start_time,
            end_time=end_time
        )

    def get_base(self) -> TimeslotBase:
        return TimeslotBase(
            id=self.id,
            school_id=self.school_id,
            timeslot_type=self.timeslot_type,
            date=self.date,
            timeslot_number=self.timeslot_number,
        )

    def to_model(self) -> TimeslotModel:
        start_time_text = self.start_time.strftime("%H:%M")
        end_time_text = self.end_time.strftime("%H:%M")
        return TimeslotModel(
            record_type=self.record_type,
            id=self.id,
            school_id=self.school_id,

            display_name=self.display_name,
            given_name=self.given_name,
            family_name=self.family_name,
            lecture_hourly_pay=self.lecture_hourly_pay,
            office_hourly_pay=self.office_hourly_pay,

            timeslot_type=self.timeslot_type,
            start_time=start_time_text,
            end_time=end_time_text,
        )

    @classmethod
    def from_model(cls, timeslot_model: TimeslotModel) -> Self:
        date, timeslot_number = timeslot_model.get_date_timeslot_num()
        start_time = datetime.datetime.strptime(timeslot_model.start_time, "%H:%M").time()
        end_time = datetime.datetime.strptime(timeslot_model.end_time, "%H:%M").time()
        return Timeslot(
            id=timeslot_model.id,
            school_id=timeslot_model.school_id,
            timeslot_type=timeslot_model.timeslot_type,
            date=date,
            timeslot_number=timeslot_number,

            display_name=timeslot_model.display_name,
            given_name=timeslot_model.given_name,
            family_name=timeslot_model.family_name,
            lecture_hourly_pay=timeslot_model.lecture_hourly_pay,
            office_hourly_pay=timeslot_model.office_hourly_pay,

            start_time=start_time,
            end_time=end_time
        )