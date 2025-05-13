from io import BytesIO

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from pynamodb.exceptions import DoesNotExist

from api.cruds.teacher import TeacherRepo
from api.schemas.person import Teacher, TeacherBase

router = APIRouter()


@router.post("/teachers", response_model=Teacher, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher_base: TeacherBase):
    # uniqueness of display_name
    teacher_list = TeacherRepo.list(teacher_base.school_id)
    if teacher_base.display_name in [t.display_name for t in teacher_list]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"display_name '{teacher_base.display_name}' already exists.",
        )

    teacher = TeacherRepo.create(teacher_base)
    return teacher


@router.post(
    "/teachers/bulk/{school_id}",
    response_model=list[Teacher],
    status_code=status.HTTP_201_CREATED,
)
async def create_teachers_from_csv(school_id: str, file: UploadFile = File(...)):
    buffer = BytesIO(await file.read())
    df = pd.read_csv(buffer)
    df = df.where(df.notna(), None)

    teacher_base_required_keys = [
        "display_name",
        "given_name",
        "family_name",
        "lecture_hourly_pay",
        "office_hourly_pay",
    ]
    if not all([k in df.columns for k in teacher_base_required_keys]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Required keys: {teacher_base_required_keys}",
        )

    # uniqueness of display_name
    teacher_list = TeacherRepo.list(school_id)
    if df["display_name"].isin([t.display_name for t in teacher_list]).sum() > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="display_name already exists.",
        )

    ret = [
        TeacherRepo.create(TeacherBase(school_id=school_id, **v))
        for v in df.to_dict(orient="index").values()
    ]
    return ret


@router.get(
    "/teachers/bulk/{school_id}",
    response_model=list[Teacher],
    status_code=status.HTTP_200_OK,
)
async def list_teachers(school_id: str):
    teachers = TeacherRepo.list(school_id)
    return teachers


@router.get("/teachers/{id}", response_model=Teacher, status_code=status.HTTP_200_OK)
async def get_teacher(id: str):
    try:
        teacher = TeacherRepo.get(id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher not found. id: {id}"
        )
    return teacher


@router.get(
    "/teachers/sub/{sub}", response_model=Teacher, status_code=status.HTTP_200_OK
)
async def get_teacher_from_sub(sub: str):
    try:
        teacher = TeacherRepo.get_from_sub(sub)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Teacher not found. sub: {sub}",
        )
    return teacher


@router.put("/teachers/{id}", response_model=Teacher, status_code=status.HTTP_200_OK)
async def update_teacher(id: str, teacher_base: TeacherBase):
    try:
        teacher = TeacherRepo.update(id, teacher_base)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher not found. id: {id}"
        )
    return teacher


@router.delete("/teachers/{id}", response_model=Teacher, status_code=status.HTTP_200_OK)
async def delete_teacher(id: str):
    try:
        teacher = TeacherRepo.delete(id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher not found. id: {id}"
        )
    return teacher
