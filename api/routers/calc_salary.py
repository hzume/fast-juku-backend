from fastapi import APIRouter

router = APIRouter()

@router.post("/calc_salary")
async def upload_class_sheet():
    pass

@router.get("/calc_salary/calculate")
async def calculate_salary():
    pass
