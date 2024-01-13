from api.db import TeacherModel
from api.schemas.person import Teacher, TeacherBase

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
    def get_from_sub(cls, sub: str) -> Teacher:
        try :
            teacher_model = TeacherModel.query("teacher", filter_condition = (TeacherModel.sub==sub)).next()
        except StopIteration:
            return Teacher(
                id="",
                display_name="Guest",
                given_name="user",
                family_name="Guest",
                school_id="",
                lecture_hourly_pay=0.0,
                office_hourly_pay=0.0,
                trans_fee=0.0,
                teacher_type="teacher",
                sub=sub,
            )

        teacher = Teacher.from_model(teacher_model)
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
    