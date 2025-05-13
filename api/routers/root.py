import io

import openpyxl as xl
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class RootRequest(BaseModel):
    name: str


@router.get("/")
async def root():
    return {"message": "hello world"}


@router.post("/test/")
async def post_root(file: UploadFile = File(...)):
    try:
        content = await file.read()
        wb = xl.load_workbook(io.BytesIO(content))
        ws = wb["4月1日"]
        return JSONResponse(content={"data": ws["A1"].value})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
