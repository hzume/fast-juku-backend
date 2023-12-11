import datetime
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection, IncludeProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, UnicodeSetAttribute, BooleanAttribute, MapAttribute, ListAttribute, DiscriminatorAttribute


class SchoolIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'school_id_index'
        read_capacity_units = 5
        write_capacity_units = 5
        projection = AllProjection()

    school_id = UnicodeAttribute(hash_key=True)
    record_type = UnicodeAttribute(range_key=True)


class DBModelBase(Model):
    class Meta:
        table_name = 'main_table'

    record_type = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    school_id = UnicodeAttribute()
    cls = DiscriminatorAttribute()
    school_id_index = SchoolIndex()
    timestamp = UnicodeAttribute()

    
    display_name = UnicodeAttribute(null=True)
    given_name = UnicodeAttribute(null=True)
    family_name = UnicodeAttribute(null=True)
    lecture_hourly_pay = NumberAttribute(null=True)
    office_hourly_pay = NumberAttribute(null=True)

    timeslot_type = UnicodeAttribute(null=True)
    start_time = UnicodeAttribute(null=True)
    end_time = UnicodeAttribute(null=True)

    school_name = UnicodeAttribute(null=True)


# record_type = "timeslot#2023-07-14#1"
# id = UID
# ある講師が2023年7月14日の1限目に担当する講義など
class TimeslotModel(DBModelBase, discriminator="timeslot"):
    year = NumberAttribute()
    month = NumberAttribute()
    day = NumberAttribute()
    timeslot_number = NumberAttribute()

    timeslot_type = UnicodeAttribute()
    start_time = UnicodeAttribute()
    end_time = UnicodeAttribute()


# record_type = "teacher"
# id = UID
# 講師の情報

# record_type = "teacher#2023-07"
# 2023年7月時点での講師の情報
class TeacherModel(DBModelBase, discriminator="teacher"):
    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()
    trans_fee = NumberAttribute()
    teacher_type = UnicodeAttribute()
    
    year = NumberAttribute(null=True)
    month = NumberAttribute(null=True)


# record_type = "meta"
# id = school_id
# 塾ごとのメタ情報。各講義の開始時刻・終了時刻など
class MetaModel(DBModelBase, discriminator="meta"):
    school_name = UnicodeAttribute()
