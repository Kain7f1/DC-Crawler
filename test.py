import utility_module as util
from datetime import datetime
import pandas as pd

# [특정 키워드 포함된 데이터 지우기]
# util.delete_rows(delete_keyword="코스", column="text")

# [url log 합치기]
keyword = "LG화학"
gall_name_list = [
    "코스피", "실전주식투자", "미국주식", "해외주식", "주식",
    "재테크", "S_P500", "다우", "나스닥", "증권",
    "금융", "해외선물", "해외선물실전투자", "국내선물옵션", "캠퍼스개미"
]


###############################################################################################################
# merge_url_crawling_results()
# 기능 : 2개 이상의 키워드로 url 크롤링 했을 경우, 결과를 합치는 함수
def merge_url_crawling_results(gall_name_list_):
    start_time = datetime.now().replace(microsecond=0)
    str_start_time = str(start_time)[2:10].replace("-", "") + "_" + str(start_time)[11:].replace(":", "")

    # [1. url crawling file 합치기 + 중복제거]
    # for gall_name in gall_name_list_:
    #     util.merge_csv_files(save_file_name=f"merged_url_crawling_result_{keyword}_{gall_name}",
    #                          read_folder_path_="./url/crawling_result",
    #                          save_folder_path_="./url/merged_files",
    #                          keyword=f"{gall_name}",
    #                          subset='number')

    # [2. url crawling log 합치기]
    url_log_folder_path = "./url/crawling_log"
    read_file_encoding = 'utf-8'
    save_file_encoding = 'utf-8'

    for gall_name in gall_name_list_:
        # 2-1. 폴더 내의 파일을 검색한다
        log_files = util.read_files(folder_path_=url_log_folder_path, keyword=gall_name, endswith='.csv')
        log_file_paths = []
        for log_file in log_files:
            log_file_paths.append(f"{url_log_folder_path}/{log_file}")
        merged_df = sum_dataframes(log_file_paths, encoding=read_file_encoding)

        save_file_path = f"{url_log_folder_path}/merged_crawling_log_{keyword}_{gall_name}_{str_start_time}.csv"
        # 2-3. df를 csv로 만든다
        merged_df.to_csv(save_file_path, encoding=save_file_encoding, index=False)


############################
# 기능 : df를
def sum_dataframes(file_paths, encoding='utf-8'):
    # 합쳐진 데이터를 저장할 빈 데이터프레임 생성
    merged_df = pd.DataFrame()

    # 각 파일별로 데이터를 읽어서 병합
    for path in file_paths:
        # 현재 파일 데이터를 읽음
        df = pd.read_csv(path, encoding=encoding)

        # 정수형 컬럼들의 합을 계산하여 누적
        int_cols = df.select_dtypes(include=['int64']).columns
        if merged_df.empty:
            # 문자열 컬럼은 첫 번째 파일에서 가져옴
            merged_df = df.select_dtypes(include=['object']).iloc[0].to_frame().T
            # 정수형 컬럼의 합계를 새로운 데이터프레임에 추가
            merged_df = pd.concat([merged_df, df[int_cols].sum().to_frame().T], axis=1)
        else:
            # 정수형 컬럼의 합계를 기존 데이터프레임에 추가
            merged_df[int_cols] += df[int_cols].sum()

    # 병합된 데이터프레임의 인덱스를 재설정
    merged_df.reset_index(drop=True, inplace=True)

    return merged_df


merge_url_crawling_results(gall_name_list)