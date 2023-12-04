from typing import Self
import uuid
from pydantic import BaseModel
import datetime

from api.db import MetaModel

class MetaBase(BaseModel):
    school_name: str
    timeslot_start_times: list[datetime.time]
    timeslot_end_times: list[datetime.time]

    def get_times_text(self) -> tuple[list[str], list[str]]:
        start_times_text = [start_time.strftime("%H:%M") for start_time in self.timeslot_start_times]
        end_times_text = [end_time.strftime("%H:%M") for end_time in self.timeslot_end_times]
        return start_times_text, end_times_text
    
    @classmethod
    def get_times_datetime(cls, meta_model: MetaModel) -> tuple[list[datetime.time], list[datetime.time]]:
        start_times_text = meta_model.timeslot_start_times
        end_times_text = meta_model.timeslot_end_times
        start_times = [datetime.datetime.strptime(start_time_text, "%H:%M").time() for start_time_text in start_times_text]
        end_times = [datetime.datetime.strptime(end_time_text, "%H:%M").time() for end_time_text in end_times_text]
        return start_times, end_times
    
    def start_time(self, timeslot_number: int) -> datetime.time:
        return self.timeslot_start_times[timeslot_number-1]
    
    def end_time(self, timeslot_number: int) -> datetime.time:
        return self.timeslot_end_times[timeslot_number-1]

class Meta(MetaBase):
    school_id: str

    @classmethod
    def create(cls, meta_base: MetaBase) -> Self:
        school_id = uuid.uuid4().hex
        meta = Meta(school_id=school_id, **meta_base.model_dump())
        return meta
    
    def update(self, meta_base: MetaBase) -> Self:
        return Meta(school_id=self.school_id, **meta_base.model_dump())

    def to_model(self) -> MetaModel:
        start_times, end_times = self.get_times_text()
        return MetaModel(
            record_type="meta",
            id=self.school_id,
            school_id=self.school_id,

            school_name=self.school_name,
            timeslot_start_times=start_times,
            timeslot_end_times=end_times
        )
    
    @classmethod
    def from_model(cls, meta_model: MetaModel) -> Self:
        start_times, end_times = cls.get_times_datetime(meta_model)
        return Meta(
            school_id=meta_model.school_id,
            school_name=meta_model.school_name,
            timeslot_start_times=start_times,
            timeslot_end_times=end_times
        )
    