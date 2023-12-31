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

digest_size = 10
    
class_times = {
        "2:00-3:20":1, 
        "3:30-4:50":2, 
        "5:00-6:20":3, 
        "6:30-7:50":4, 
        "8:00-9:20":5
    }