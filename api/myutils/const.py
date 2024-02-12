class CellBlock:
    BLOCK_SIZE = 3
    MAX_BLOCKS_ROW = 25
    MAX_BLOCKS_COL = 15

    BLOCK_NAME_IDX = 0
    BLOCK_CELL1_IDX = 1
    BLOCK_CELL2_IDX = 2

    INFO_COL = 1
    INFO_DATE_IDX = 0
    INFO_TIMESLOTNUM_IDX = 1
    INFO_TIME_IDX = 2

DIGEST_SIZE = 10

PREPARE_TIME = 10 # 10分
    
LECTURE_TIMES_TO_NUMBER = {
        "2:00-3:20":1, 
        "3:30-4:50":2, 
        "5:00-6:20":3, 
        "6:30-7:50":4, 
        "8:00-9:20":5
    }

NUMBER_TO_LECTURE_TIMES = {v: k for k, v in LECTURE_TIMES_TO_NUMBER.items()}

GENSEN_PATH = "api/data/gensen-r5.csv"

class Payslip:
    YEAR_CELL = "F2"
    MONTH_CELL = "H2"

    SCHOOL_NAME = "E5"
    FULL_NAME = "H5"

    TIMESLOT_START_ROW = "9"
    TIMESLOT_START_COL = "3"

    