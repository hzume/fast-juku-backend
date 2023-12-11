import datetime
from unicodedata import normalize

from pydantic import BaseModel, field_validator

class YearMonth(BaseModel):
    year: int
    month: int | None = None

    @field_validator("month")
    @classmethod
    def month_range(cls, v):
        if v < 1 or v > 12:
            raise ValueError(f"month must be in range 1-12, but {v}")
        return v
    
    @field_validator("year")
    @classmethod
    def year_range(cls, v):
        if v < 1000 or v > 9999:
            raise ValueError(f"year must be in range 1000-9999, but {v}")
        return v
    
    @property
    def text(self) -> str:
        if self.month is None:
            return f"{self.year}"
        return f"{self.year}-{self.month:02}"


def excel_date_to_datetime(excel_date: int) -> datetime.date:
    return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=excel_date)).date()

def str2int_timeslot_num(timeslot_num_str: str) -> int:
    trans_dict = {
        "①": 1,
        "②": 2,
        "③": 3,
        "④": 4,
        "⑤": 5,
        "⑥": 6,
        "⑦": 7,
        "⑧": 8,
        "⑨": 9,
    }

    if timeslot_num_str not in trans_dict.keys():
        raise ValueError(f"timeslot number must be ①-⑨, but {timeslot_num_str}")
    
    return trans_dict[timeslot_num_str]

def get_start_end_time(time: str) -> tuple[datetime.time, datetime.time]:
    time = normalize("NFKC", time)
    start_time_str, end_time_str = time.split("-")
    start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
    return start_time, end_time