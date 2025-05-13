from fastapi import APIRouter, status

from api.cruds.meta import MetaRepo
from api.cruds.teacher import TeacherRepo
from api.schemas.utils import User

router = APIRouter()

@router.get("/users/{sub}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(sub: str):    
    teacher = TeacherRepo.get_from_sub(sub)
    meta = MetaRepo.get(teacher.school_id)
    return User(
        id=teacher.id,
        sub=teacher.sub,
        given_name=teacher.given_name,
        family_name=teacher.family_name,
        school_id=teacher.school_id,
        school_name=meta.school_name,
        role=teacher.teacher_type,
    )
    
