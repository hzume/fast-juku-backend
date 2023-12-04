from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RootRequest(BaseModel):
    name: str

@router.get("/")
async def root():
    return {"message":"hello, root"}

@router.post("/")
async def post_root(req: RootRequest):
    return {"message":f"hello, {req.name}"}    

@router.get("/hello")
async def hello():
    return {"message":"hello world"}