from pynamodb.attributes import (
    UnicodeAttribute,
)

from api.models.base import DBModelBase


# 生徒の情報
class StudentModel(DBModelBase, discriminator="student"):
    person_id = UnicodeAttribute()
    school_id = UnicodeAttribute()
    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()

    grade = UnicodeAttribute()
    incharge_teacher_id = UnicodeAttribute()