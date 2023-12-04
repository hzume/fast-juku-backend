from fastapi import APIRouter
from schemas.person import Teacher, TeacherBase
import uuid
from cruds.teacher import TeacherRepo

router = APIRouter()
repo = TeacherRepo()

@router.post("/teachers", response_model=Teacher)
async def create_teacher(teacher_base: TeacherBase):
    teacher = repo.create(teacher_base)
    return teacher

@router.get("/teachers", response_model=list[Teacher])
async def list_teachers(school_name: str):
    teachers = repo.list(school_name)
    return teachers

@router.get("/teachers/{id}", response_model=Teacher)
async def get_teacher(id: str):
    teacher = repo.get(id)
    return teacher

@router.put("/teachers/{id}", response_model=Teacher)
async def update_teacher(id: str, teacher_base: TeacherBase):
    teacher = repo.update(id, teacher_base)
    return teacher

@router.delete("/teachers/{id}")
async def delete_teacher(id: str):
    ret = repo.delete(id)
    return ret
