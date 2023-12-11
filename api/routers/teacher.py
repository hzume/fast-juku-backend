from fastapi import APIRouter
import uuid

from api.schemas.person import Teacher, TeacherBase
from api.cruds.teacher import TeacherRepo

router = APIRouter()


@router.post("/teachers", response_model=Teacher)
async def create_teacher(teacher_base: TeacherBase):
    teacher = TeacherRepo.create(teacher_base)
    return teacher

@router.get("/teachers", response_model=list[Teacher])
async def list_teachers(school_id: str):
    teachers = TeacherRepo.list(school_id)
    return teachers

@router.get("/teachers/{id}", response_model=Teacher)
async def get_teacher(id: str):
    teacher = TeacherRepo.get(id)
    return teacher

@router.put("/teachers/{id}", response_model=Teacher)
async def update_teacher(id: str, teacher_base: TeacherBase):
    teacher = TeacherRepo.update(id, teacher_base)
    return teacher

@router.delete("/teachers/{id}")
async def delete_teacher(id: str):
    ret = TeacherRepo.delete(id)
    return ret
