from fastapi import APIRouter, HTTPException, status
from pynamodb.exceptions import DoesNotExist

from api.cruds.meta import MetaRepo
from api.schemas.meta import Meta, MetaBase

router = APIRouter()


@router.post("/metas", response_model=Meta, status_code=status.HTTP_201_CREATED)
async def create_meta(meta_base: MetaBase) -> Meta:
    meta_list = MetaRepo.list()
    if meta_base.school_name in [m.school_name for m in meta_list]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"School name {meta_base.school_name} already exists."
        )

    meta = MetaRepo.create(meta_base)
    return meta


@router.get("/metas/{school_id}", response_model=Meta, status_code=status.HTTP_200_OK)
async def get_meta(school_id: str) -> Meta:
    try:
        meta = MetaRepo.get(school_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"School not found. school_id: {school_id}"
        )
    return meta


@router.get("/metas", response_model=list[Meta], status_code=status.HTTP_200_OK)
async def list_metas() -> list[Meta]:
    metas = MetaRepo.list()
    return metas


@router.put("/metas/{school_id}", response_model=Meta, status_code=status.HTTP_200_OK)
async def update_meta(school_id: str, meta_base: MetaBase) -> Meta:
    try:
        meta = MetaRepo.update(school_id, meta_base)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"School not found. school_id: {school_id}"
        )
    return meta


@router.delete("/metas/{school_id}", response_model=Meta, status_code=status.HTTP_200_OK)
async def delete_meta(school_id: str) -> Meta:
    try:
        meta = MetaRepo.delete(school_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"School not found. school_id: {school_id}"
        )
    return meta
