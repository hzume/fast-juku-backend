from typing import Self
import uuid
from pydantic import BaseModel
import datetime

from api.db import MetaModel

class MetaBase(BaseModel):
    school_name: str
    

class Meta(MetaBase):
    school_id: str

    @classmethod
    def create(cls, meta_base: MetaBase) -> Self:
        school_id = uuid.uuid4().hex
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
    