from fastapi import APIRouter, Header
from pydantic import BaseModel

router = APIRouter()

class RootRequest(BaseModel):
    name: str

@router.get("/")
async def root():
    return {"message":"hello world"}

@router.post("/")
async def post_root(req: RootRequest):
    return {"message":f"hello, {req.name}"}    
