import uuid
from db import MetaModel
from schemas.meta import Meta, MetaBase


class MetaRepo:
    @classmethod
    def create(cls, meta_base: MetaBase) -> Meta:
        meta = Meta.create(meta_base)
        regist_meta = meta.to_model()
        regist_meta.save()
        return meta

    @classmethod
    def get(cls, school_id: str) -> Meta:
        meta = Meta.from_model(MetaModel.get("meta", school_id))
        return meta
    
    @classmethod
    def list(cls) -> list[Meta]:
        metas = [
            Meta.from_model(meta_model) for meta_model 
            in MetaModel.query("meta")
        ]
        return metas

    @classmethod
    def update(cls, school_id: str, meta_base: MetaBase) -> Meta:
        old_meta = cls.get(school_id)
        new_meta = old_meta.update(meta_base)
        regist_meta = new_meta.to_model()
        regist_meta.save()
        return new_meta

    @classmethod
    def delete(cls, school_id: str) -> Meta:
        meta = cls.get(school_id)
        meta_model = meta.to_model()
        meta_model.delete()
        return meta