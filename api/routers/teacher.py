from fastapi import APIRouter
from schemas.person import Teacher, TeacherBase

router = APIRouter()

@router.post("/teachers", response_model=Teacher)
async def create_teacher(teacher_body: TeacherBase):
    return Teacher(id="id", **teacher_body.model_dump())

@router.get("/teachers", response_model=list[Teacher])
async def list_teachers():
    return {"message": "list of teachers"}

@router.get("/teachers/{id}", response_model=Teacher)
async def get_teacher(id: str):
    pass

@router.put("/teachers/{id}", response_model=Teacher)
async def update_teacher_config(id: str, teacher_body: TeacherBase):
    return Teacher(id=id, **teacher_body.model_dump())

@router.delete("/teachers/{id}")
async def delete_teacher(id: str):
    return 

