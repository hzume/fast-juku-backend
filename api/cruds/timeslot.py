import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from schemas.timeslot import Timeslot, TimeslotBase
from db import TimeslotModel
from cruds.meta import MetaRepo
from cruds.teacher import TeacherRepo
from functools import singledispatch


class YearMonth(BaseModel):
    year: int
    month: Optional[int] = None

    @field_validator("month")
    @classmethod
    def month_range(cls, v):
        if v < 1 or v > 12:
            raise ValueError(f"month must be in range 1-12, but {v}")
        return v
    
    @field_validator("year")
    @classmethod
    def year_range(cls, v):
        if v < 1000 or v > 9999:
            raise ValueError(f"year must be in range 1000-9999, but {v}")
        return v
    
    @property
    def text(self) -> str:
        return f"{self.year}-{self.month:02}"


class TimeslotRepo: 
    @classmethod
    def create(cls, timeslot_base: TimeslotBase) -> Timeslot:
        meta = MetaRepo.get(timeslot_base.school_id)
        teacher = TeacherRepo.get(timeslot_base.id)
        timeslot = Timeslot.create(timeslot_base, meta, teacher)
        regist_timeslot = timeslot.to_model()
        regist_timeslot.save()
        return timeslot

    @classmethod
    def list_monthly(cls, school_id: str, year_month: YearMonth) -> list[Timeslot]:
        record_type = f"timeslot#{year_month.text}"
        timeslots: list[TimeslotModel] = [
            Timeslot.from_model(timeslot_model) for timeslot_model
            in TimeslotModel.school_id_index.query(school_id, TimeslotModel.record_type.startswith(record_type))
        ]
        return timeslots

    @singledispatch
    @classmethod
    def get(cls, id: str, date: datetime.date, timeslot_number: int) -> Timeslot:
        record_type = f"timeslot#{date}#{timeslot_number}"
        timeslot = Timeslot.from_model(TimeslotModel.get(record_type, id, record_type))
        return timeslot

    @get.register
    @classmethod
    def get_from_base(cls, timeslot_base: TimeslotBase) -> Timeslot:
        return cls.get(timeslot_base.id, timeslot_base.date, timeslot_base.timeslot_number)

    @classmethod
    def update(cls, timeslot_base: TimeslotBase) -> Timeslot:
        old_timeslot = cls.get(timeslot_base)
        meta = MetaRepo.get(timeslot_base.school_id)
        teacher = TeacherRepo.get(timeslot_base.id)
        new_timeslot = old_timeslot.update(timeslot_base, meta, teacher)
        regist_timeslot = new_timeslot.to_model()
        regist_timeslot.save()
        return new_timeslot

    @singledispatch
    @classmethod
    def delete(cls, id: str, date: datetime.date, timeslot_number: int):
        timeslot = cls.get(id, date, timeslot_number)
        timeslot_model = timeslot.to_model()
        timeslot_model.delete()
        return timeslot
    
    @delete.register
    @classmethod
    def delete_from_base(cls, timeslot_base: TimeslotBase):
        return cls.delete(timeslot_base.id, timeslot_base.date, timeslot_base.timeslot_number)
