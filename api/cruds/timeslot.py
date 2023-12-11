import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
from functools import singledispatch

from api.schemas.timeslot import Timeslot, TimeslotBase
from api.db import TimeslotModel
from api.cruds.meta import MetaRepo
from api.cruds.teacher import TeacherRepo
from api.myutils.utilfunc import YearMonth


class TimeslotRepo: 
    @classmethod
    def create(cls, id: str, timeslot_base: TimeslotBase) -> Timeslot:
        timeslot = Timeslot.create(id, timeslot_base)
        regist_timeslot = timeslot.to_model()
        regist_timeslot.save()
        return timeslot
    
    @classmethod
    def list_by_teacher(cls, school_id: str, teacher_id: str, year_month: YearMonth) -> list[Timeslot]:
        record_type = f"timeslot#{year_month.text}"
        timeslots = [
            Timeslot.from_model(timeslot_model) for timeslot_model
            in TimeslotModel.school_id_index.query(school_id, TimeslotModel.record_type.startswith(record_type), (TimeslotModel.id == teacher_id))
        ]
        return timeslots

    @classmethod
    def list(cls, school_id: str, year_month: YearMonth) -> list[Timeslot]:
        record_type = f"timeslot#{year_month.text}"
        timeslots = [
            Timeslot.from_model(timeslot_model) for timeslot_model
            in TimeslotModel.school_id_index.query(school_id, TimeslotModel.record_type.startswith(record_type))
        ]
        return timeslots
  
    @classmethod
    def get(cls, id: str, date: datetime.date, timeslot_number: int) -> Timeslot:
        record_type = f"timeslot#{date}#{timeslot_number}"
        timeslot = Timeslot.from_model(TimeslotModel.get(record_type, id))
        return timeslot

    @classmethod
    def get_from_base(cls, id: str, timeslot_base: TimeslotBase) -> Timeslot:
        return cls.get(id, timeslot_base.date, timeslot_base.timeslot_number)

    @classmethod
    def update(cls, id: str, timeslot_base: TimeslotBase) -> Timeslot:
        old_timeslot = cls.get_from_base(id, timeslot_base)
        new_timeslot = old_timeslot.update(timeslot_base)
        regist_timeslot = new_timeslot.to_model()
        regist_timeslot.save()
        return new_timeslot

    @classmethod
    def delete(cls, id: str, date: datetime.date, timeslot_number: int):
        timeslot = cls.get(id, date, timeslot_number)
        timeslot_model = timeslot.to_model()
        timeslot_model.delete()
        return timeslot
    
    @classmethod
    def delete_from_base(cls, id: str, timeslot_base: TimeslotBase):
        return cls.delete(id, timeslot_base.date, timeslot_base.timeslot_number)
