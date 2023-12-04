import datetime
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, UnicodeSetAttribute, BooleanAttribute, MapAttribute, ListAttribute

class DBModelBase(Model):
    class Meta:
        table_name = 'MainTable'

    record_type = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    school_id = UnicodeAttribute()

class SchoolIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'school_id-index'
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    school_id = UnicodeAttribute(hash_key=True)
    record_type = UnicodeAttribute(range_key=True)

# record_type = "timeslot#2023-07-14#1"
# id = UID
# ある講師が2023年7月14日の1限目に担当する講義など
class TimeslotModel(DBModelBase):
    timeslot_type = UnicodeAttribute()

    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()

    start_time = UnicodeAttribute()
    end_time = UnicodeAttribute()

    school_id_index = SchoolIndex()

    def get_date_timeslot_num(self) -> tuple[datetime.date, int]:
        _, date, timeslot_number = self.record_type.split("#")
        date = datetime.date.fromisoformat(date)
        timeslot_number = int(timeslot_number)
        return date, timeslot_number


# record_type = "teacher"
# id = UID
# 講師の情報
class TeacherModel(DBModelBase):
    display_name = UnicodeAttribute()
    given_name = UnicodeAttribute()
    family_name = UnicodeAttribute()
    lecture_hourly_pay = NumberAttribute()
    office_hourly_pay = NumberAttribute()

# record_type = "meta"
# id = school_id
# 塾ごとのメタ情報。各講義の開始時刻・終了時刻など
class MetaModel(DBModelBase):
    school_name = UnicodeAttribute()
    timeslot_start_times = ListAttribute(of=UnicodeAttribute)
    timeslot_end_times = ListAttribute(of=UnicodeAttribute)
