from fastapi import APIRouter
from api.cruds.meta import MetaRepo
from api.schemas.meta import MetaBase, Meta

router = APIRouter()

@router.post("/metas", response_model=Meta)
async def create_meta(meta_base: MetaBase) -> Meta:
    meta = MetaRepo.create(meta_base)
    return meta

@router.get("/metas/{school_id}", response_model=Meta)
async def get_meta(school_id: str) -> Meta:
    meta = MetaRepo.get(school_id)
    return meta

@router.put("/metas/{school_id}", response_model=Meta)
async def update_meta(school_id: str, meta_base: MetaBase) -> Meta:
    meta = MetaRepo.update(school_id, meta_base)
    return meta

@router.delete("/metas/{school_id}", response_model=Meta)
async def delete_meta(school_id: str) -> Meta:
    meta = MetaRepo.delete(school_id)
    return meta