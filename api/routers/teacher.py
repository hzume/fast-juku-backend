from fastapi import APIRouter

router = APIRouter()

@router.post("/teachers")
async def create_teacher():
    pass

@router.get("/teachers")
async def list_teachers():
    pass

@router.get("/teachers/{teacherId}")
async def mypage():
    pass

@router.put("/teachers/{teacherId}")
async def update_teacher_config():
    pass

@router.delete("/teachers/{teacherId}")
async def delete_teacher():
    pass

