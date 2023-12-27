from io import BytesIO
from fastapi import APIRouter, File, UploadFile
import uuid
import pandas as pd

from api.schemas.person import Teacher, TeacherBase
from api.cruds.teacher import TeacherRepo


router = APIRouter()
@router.post("/teachers", response_model=Teacher)
async def create_teacher(teacher_base: TeacherBase):
    teacher = TeacherRepo.create(teacher_base)
    return teacher

@router.post("/teachers/bulk", response_model=list[Teacher])
async def create_teachers_from_csv(school_id: str, file: UploadFile = File(...)):
    buffer = BytesIO(await file.read())
    df = pd.read_csv(buffer)
    df = df.where(df.notna(), None)
    ret = [TeacherRepo.create(TeacherBase(school_id=school_id, **v))
           for v in df.to_dict(orient="index").values()]
    return ret

@router.get("/teachers", response_model=list[Teacher])
async def list_teachers(school_id: str):
    teachers = TeacherRepo.list(school_id)
    return teachers

@router.get("/teachers/{id}", response_model=Teacher)
async def get_teacher(id: str):
    teacher = TeacherRepo.get(id)
    return teacher

@router.get("/teachers/sub/{sub}", response_model=Teacher)
async def get_teacher_from_sub(sub: str):
    teacher = TeacherRepo.get_from_sub(sub)
    return teacher

@router.put("/teachers/{id}", response_model=Teacher)
async def update_teacher(id: str, teacher_base: TeacherBase):
    teacher = TeacherRepo.update(id, teacher_base)
    return teacher

@router.delete("/teachers/{id}")
async def delete_teacher(id: str):
    ret = TeacherRepo.delete(id)
    return ret
