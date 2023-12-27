from hashlib import shake_128

from api.db import TeacherModel
from api.schemas.person import Teacher, TeacherBase
from api.myutils.utilfunc import YearMonth
from api.myutils.const import digest_size

class TeacherRepo:
    @classmethod
    def create(cls, teacher_base: TeacherBase) -> Teacher:
        teacher = Teacher.create(teacher_base)
        regist_teacher = teacher.to_model()
        regist_teacher.save()
        return teacher
    
    @classmethod
    def regist(cls, teacher: Teacher) -> Teacher:
        regist_teacher = teacher.to_model()
        regist_teacher.save()
        return teacher

    @classmethod
    def list(cls, school_id: str, year_month: YearMonth | None = None) -> list[Teacher]:
        if year_month != None:
            assert isinstance(year_month, YearMonth)
            assert year_month.month != None
            teachers = [
                Teacher.from_model(teacher_model) for teacher_model 
                in TeacherModel.query(f"teacher#{year_month.text}", filter_condition = (TeacherModel.school_id==school_id))
            ]
            return teachers
        else:
            teachers = [
                Teacher.from_model(teacher_model) for teacher_model 
                in TeacherModel.query("teacher", filter_condition = (TeacherModel.school_id==school_id))
            ]
            return teachers

    @classmethod
    def get(cls, id: str) -> Teacher:
        teacher = Teacher.from_model(TeacherModel.get("teacher", id))
        return teacher
    
    @classmethod
    def get_from_sub(cls, sub: str) -> Teacher:
        teacher_model = TeacherModel.query("teacher", filter_condition = (TeacherModel.sub==sub)).next()
        teacher = Teacher.from_model(teacher_model)
        return teacher

    @classmethod
    def update(cls, id, teacher_base: TeacherBase, year_month: YearMonth | None = None) -> Teacher:
        old_teacher = cls.get(id)
        new_teacher = old_teacher.update(teacher_base, year_month)
        regist_teacher = new_teacher.to_model()
        regist_teacher.save()
        return new_teacher

    @classmethod
    def delete(cls, id) -> Teacher:
        teacher_model = TeacherModel.get("teacher", id)
        teacher = Teacher.from_model(teacher_model)
        teacher_model.delete()
        return teacher
    