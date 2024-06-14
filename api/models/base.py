
from pynamodb.attributes import (
    BooleanAttribute,
    DiscriminatorAttribute,
    ListAttribute,
    MapAttribute,
    NumberAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model


class DBModelBase(Model):
    class Meta:
        # table_name = os.environ["TABLE_NAME"]
        # region = os.environ["REGION"]
        table_name = "attendance-management"
        region = "ap-northeast-1"
        # host = 'http://localhost:8000'
        
        read_capacity_units = 25
        write_capacity_units = 25

    p_key = UnicodeAttribute(hash_key=True)
    s_key = UnicodeAttribute(range_key=True)
    cls = DiscriminatorAttribute()
    timestamp = UnicodeAttribute()    
    

# ある講師が2023年7月14日の1限目に担当する講義など
class TimeslotMap(MapAttribute):
    year = NumberAttribute()
    month = NumberAttribute()
    day = NumberAttribute()
    start_time = UnicodeAttribute()
    end_time = UnicodeAttribute()
    timeslot_number = NumberAttribute()
    timeslot_type = UnicodeAttribute() 




# record_type = "attendance#2023-07"
# id = teacher_id
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
    remark = UnicodeAttribute(null=True)

    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()
    trans_fee = NumberAttribute()
    fixed_salary = NumberAttribute(null=True)
    teacher_type = UnicodeAttribute()
    sub = UnicodeAttribute(null=True)


# record_type = "meta"
# id = school_id
# 塾ごとのメタ情報。各講義の開始時刻・終了時刻など
class SchoolModel(DBModelBase, discriminator="school"):
    school_name = UnicodeAttribute()
