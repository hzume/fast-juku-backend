from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message":"hello, world"}

@router.get("/hello")
async def hello():
    return {"message":"hello world"}