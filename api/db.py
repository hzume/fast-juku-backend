from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, UnicodeSetAttribute, BooleanAttribute

class MainTable(Model):
    class Meta:
        table_name = 'MainTable'
        region = 'ap-northeast-3'
        host = 'http://localhost:8000'
    UID = UnicodeAttribute(hash_key=True)
    Type = UnicodeAttribute(range_key=True)
    GivenName = UnicodeAttribute()
    FamilyName = UnicodeAttribute()
    SchoolName = UnicodeAttribute()
    ClassHourlyPay = NumberAttribute()
    OfficeHourlyPay = NumberAttribute()
    OfficeWorkTime = NumberAttribute()
    