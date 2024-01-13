import datetime
from pynamodb.models import Model
from pynamodb.indexes import LocalSecondaryIndex, GlobalSecondaryIndex, AllProjection, IncludeProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, UnicodeSetAttribute, BooleanAttribute, MapAttribute, ListAttribute, DiscriminatorAttribute


class SchoolIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'school_id_index'
        read_capacity_units = 25
        write_capacity_units = 25
        projection = AllProjection()

    school_id = UnicodeAttribute(hash_key=True)
    record_type = UnicodeAttribute(range_key=True)


class SubIndex(LocalSecondaryIndex):
    class Meta:
        index_name = 'sub_index'
        read_capacity_units = 25
        write_capacity_units = 25
        projection = AllProjection()

    record_type = UnicodeAttribute(hash_key=True)
    sub = UnicodeAttribute(range_key=True)

class DBModelBase(Model):
    class Meta:
        table_name = 'main_table'
        region = 'ap-northeast-3'
        
        read_capacity_units = 25
        write_capacity_units = 25

    record_type = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    school_id = UnicodeAttribute()
    cls = DiscriminatorAttribute()
    school_id_index = SchoolIndex()
    sub_index = SubIndex()
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
    
    sub = UnicodeAttribute(null=True)


# record_type = "timeslot#2023-07-14#1"
# id = UID
# ある講師が2023年7月14日の1限目に担当する講義など
class TimeslotMap(MapAttribute):
    day = NumberAttribute()
    start_time = UnicodeAttribute()
    end_time = UnicodeAttribute()
    timeslot_number = NumberAttribute()
    timeslot_type = UnicodeAttribute()


# record_type = "attendance#2023-07"
class MonthlyAttendanceModel(DBModelBase, discriminator="timeslot"):
    year = NumberAttribute()
    month = NumberAttribute()
    timeslot_list = ListAttribute(of=TimeslotMap)

    daily_lecture_amount = ListAttribute(of=NumberAttribute)
    daily_office_amount = ListAttribute(of=NumberAttribute)
    daily_latenight_amount = ListAttribute(of=NumberAttribute)
    daily_over_eight_hour_amount = ListAttribute(of=NumberAttribute)
    daily_attendance = ListAttribute(of=BooleanAttribute)

    monthly_gross_salary = NumberAttribute()
    monthly_tax_amount = NumberAttribute()
    monthly_trans_fee = NumberAttribute()
    extra_payment = NumberAttribute()

    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()
    trans_fee = NumberAttribute()
    teacher_type = UnicodeAttribute()
    sub = UnicodeAttribute(null=True)


# record_type = "teacher"
# id = UID
# 講師の情報
class TeacherModel(DBModelBase, discriminator="teacher"):
    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()
    trans_fee = NumberAttribute()
    teacher_type = UnicodeAttribute()

    sub = UnicodeAttribute(null=True)

# record_type = "meta"
# id = school_id
# 塾ごとのメタ情報。各講義の開始時刻・終了時刻など
class MetaModel(DBModelBase, discriminator="meta"):
    school_name = UnicodeAttribute()
