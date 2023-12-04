from db import TeacherModel
from schemas.person import Teacher, TeacherBase
import uuid

class TeacherRepo:
    @classmethod
    def create(cls, teacher_base: TeacherBase) -> Teacher:
        teacher = Teacher.create(teacher_base)
        regist_teacher = teacher.to_model()
        regist_teacher.save()
        return teacher

    @classmethod
    def list(cls, school_id: str) -> list[Teacher]:
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
    def update(cls, id, teacher_base: TeacherBase) -> Teacher:
        old_teacher = cls.get(id)
        new_teacher = old_teacher.update(teacher_base)
        regist_teacher = new_teacher.to_model()
        regist_teacher.save()
        return new_teacher

    @classmethod
    def delete(cls, id) -> Teacher:
        teacher_model = TeacherModel.get("teacher", id)
        teacher = Teacher.from_model(teacher_model)
        teacher_model.delete()
        return teacher
    