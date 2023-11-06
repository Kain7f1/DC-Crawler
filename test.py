import utility_module as util

# [특정 키워드 포함된 데이터 지우기]
# util.delete_rows(delete_keyword="코스", column="text")

# [url log 합치기]
keyword = "엔솔"
gall_name_list = [
    "코스피", "실전주식투자", "미국주식", "해외주식", "주식",
    "재테크", "S_P500", "다우", "나스닥", "증권",
    "금융", "해외선물", "해외선물실전투자", "국내선물옵션", "캠퍼스개미"
]


###############################################################################################################
# merge_url_crawling_results()
# 기능 : 2개 이상의 키워드로 url 크롤링 했을 경우, 결과를 합치는 함수
def merge_url_crawling_results(gall_name_list_):
    # [1. url crawling file 합치기 + 중복제거]
    for gall_name in gall_name_list_:
        util.merge_csv_files(save_file_name=f"merged_url_crawling_result_{keyword}_{gall_name}",
                             read_folder_path_="./url/crawling_result",
                             save_folder_path_="./url/merged_files",
                             keyword=f"{gall_name}",
                             subset='number')

    # [2. url crawling log 합치기]
    for gall_name in gall_name_list_:
        util.merge_csv_files(save_file_name=f"merged_url_crawling_log_{keyword}_{gall_name}",
                             read_folder_path_="./url/target_log",
                             save_folder_path_="./url/merged_log",
                             keyword=f"{gall_name}")

    util.merge_csv_files(keyword=keyword,
                         save_file_name=f"merged_url_crawling_log_{keyword}",
                         read_folder_path_="./url/merged_log",
                         save_folder_path_="./crawling_result",
                         save_file_encoding='ANSI')
