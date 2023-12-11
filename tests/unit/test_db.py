import copy
import datetime
import json
from pathlib import Path
from unicodedata import normalize
import pandas as pd
import pytest
from moto import mock_dynamodb
from rich import print
import openpyxl as xl

from api import db
from api.schemas.person import Teacher, TeacherBase
from api.schemas.meta import Meta, MetaBase
from api.schemas.timeslot import Timeslot, TimeslotBase
from api.cruds.teacher import TeacherRepo
from api.cruds.meta import MetaRepo
from api.cruds.timeslot import TimeslotRepo, YearMonth
from api.routers.timeslot import make_timeslots


def load_meta(school_name: str) -> Meta:
    meta = MetaRepo.create(MetaBase(school_name=school_name))
    return meta

def load_teacher_info(path: Path, school_id: str) -> list[Teacher]:
    df = pd.read_csv(path, encoding="cp932")
    ret = [TeacherRepo.create(TeacherBase(school_id=school_id, **v))
           for v in df.to_dict(orient="index").values()]
    return ret

def load_timeslot(path: Path, school_id: str, year: int, month: int | None = None) -> list[Timeslot]:
    wb = xl.load_workbook(path, data_only=True)
    return make_timeslots(wb, school_id, year, month)

@mock_dynamodb
def test_db():
    setattr(db.DBModelBase.Meta, "host", "http://localhost:8000")
    db.DBModelBase.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

    meta = load_meta("test_school")
    teacher_list = load_teacher_info(Path("tests/data/講師情報.csv"), meta.school_id)
    teacher_dict = {teacher.display_name: teacher.id for teacher in teacher_list} 
    timeslot_list = load_timeslot(Path("tests/data/2022　新時間割表 10月分.xlsx"), meta.school_id, 2023, 7)

    # db.DBModelBase.delete_table()

