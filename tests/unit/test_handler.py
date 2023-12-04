import datetime
import json
from typing import Iterable
import pytest
from api import main
from moto import mock_dynamodb
from api import db
from api.schemas.person import TeacherBase, Teacher
from api.schemas.meta import MetaBase, Meta
from api.schemas.timeslot import TimeslotBase, Timeslot
from api.cruds.teacher import TeacherRepo
from api.cruds.meta import MetaRepo
from api.cruds.timeslot import TimeslotRepo
from rich import print

@pytest.fixture()
def bases():
    meta_base = MetaBase(**{
        "school_name": "test",
        "timeslot_start_times": [
            datetime.time(hour=9, minute=0),
            datetime.time(hour=10, minute=0),
            datetime.time(hour=11, minute=0),
            datetime.time(hour=12, minute=0),
        ],
        "timeslot_end_times": [
            datetime.time(hour=10, minute=0),
            datetime.time(hour=11, minute=0),
            datetime.time(hour=12, minute=0),
            datetime.time(hour=13, minute=0),
        ],
    })
    return {
        "meta_base": meta_base
    }


@mock_dynamodb
def test_lambda_handler(bases):
    db.DBModelBase.create_table(read_capacity_units=5, write_capacity_units=5, wait=True)

    meta_base = bases["meta_base"]
    ret = MetaRepo.create(meta_base)
    print(ret)
    assert ret.school_id is not None

    meta = MetaRepo.get(ret.school_id)
    print(meta)
    assert meta.school_id is not None

    teacher_base = TeacherBase(**{
        "display_name": "test",
        "given_name": "test",
        "family_name": "test",
        "lecture_hourly_pay": 1000,
        "office_hourly_pay": 2000,
        "school_id": meta.school_id,
    })

    ret = TeacherRepo.create(teacher_base)
    print(ret)
    assert ret.id is not None

    ret = TeacherRepo.list(meta.school_id)
    print(ret)
    assert len(ret) == 1
    id = ret[0].id

    teacher = TeacherRepo.get(id)
    print(teacher)
    assert teacher.id == id

    timeslot_base = TimeslotBase(**{
        "id": teacher.id,
        "school_id": meta.school_id,
        "timeslot_type": "lecture",
        "date": datetime.date.fromisoformat("2023-07-14"),
        "timeslot_number": 1,
    })
    ret = TimeslotRepo.create(timeslot_base)
    print(ret)
    assert ret.id is not None


@pytest.fixture()
def events():
    ret = []
    get_root = {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "requestContext": {
            "Dummy": "Dummy"
        }
    }
    create_teacher = {
        "resource": "/teachers",
        "path": "/teachers",
        "httpMethod": "POST",
        "requestContext": {
            "Dummy": "Dummy"
        },
        "body": json.dumps({
            "display_name": "test",
            "given_name": "test",
            "family_name": "test",
            "lecture_hourly_pay": 1000,
            "office_hourly_pay": 2000,
            "school_name": "test"
        })
    }
    list_teachers = {
        "resource": "/teachers",
        "path": "/teachers",
        "httpMethod": "GET",
        "requestContext": {
            "Dummy": "Dummy"
        },
        "queryStringParameters": {
            "school_name": "test"
        },
    }
    ret = {
        "get_root": get_root,
        "create_teacher": create_teacher,
        "list_teachers": list_teachers
    }
    return ret