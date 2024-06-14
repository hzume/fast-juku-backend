from pynamodb.attributes import (
    NumberAttribute,
    UnicodeAttribute,
)

from api.models.base import DBModelBase


class TeacherAttributes:
    teacher_id = UnicodeAttribute()
    school_id = UnicodeAttribute()
    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()
    trans_fee = NumberAttribute()
    fixed_pay = NumberAttribute()
    role = UnicodeAttribute()
    sub = UnicodeAttribute()

# p_key = teacher_id, s_key = school_id
# p_key = line id, s_key = "teacher"
# 講師の情報
class TeacherModel(DBModelBase, TeacherAttributes, discriminator="teacher"):
    pass
    
    