from typing import Self
from hashlib import shake_128
from pydantic import BaseModel
import datetime

from api.db import MetaModel
from api.myutils.const import digest_size

class MetaBase(BaseModel):
    school_name: str
    

class Meta(MetaBase):
    school_id: str

    @classmethod
    def create(cls, meta_base: MetaBase) -> Self:
        shake = shake_128()
        shake.update(meta_base.school_name.encode("utf-8"))
        school_id = shake.hexdigest(digest_size)
        return  cls(school_id=school_id, **meta_base.model_dump())
        
    def update(self, meta_base: MetaBase) -> "Meta":
        return Meta(school_id=self.school_id, **meta_base.model_dump())

    def to_model(self) -> MetaModel:
        return MetaModel(
            record_type="meta",
            id=self.school_id,
            school_id=self.school_id,
            timestamp=datetime.datetime.now().isoformat(),

            school_name=self.school_name,
        )
    
    @classmethod
    def from_model(cls, meta_model: MetaModel) -> Self:
        return cls(
            school_id=meta_model.school_id,
            school_name=meta_model.school_name,
        )
    