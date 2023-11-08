import utility_module as util
from datetime import datetime
import pandas as pd

# [특정 키워드 포함된 데이터 지우기]
# util.delete_rows(delete_keyword="코스", column="text")

keyword = "하이닉스"
gall_name_list = [
    "코스피", "실전주식투자", "미국주식", "해외주식", "주식",
    "재테크", "S_P500", "다우", "나스닥", "증권",
    "금융", "해외선물", "해외선물실전투자", "국내선물옵션", "캠퍼스개미"
]
