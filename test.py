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
    dataframes = []  # df들을 저장할 리스트
    read_file_encoding = 'utf-8'
    save_file_encoding = 'utf-8'

    # 2-1. 폴더 내의 파일을 검색한다
    csv_file_paths = read_files(folder_path_=url_log_folder_path, endswith='.csv')
    # 2-2. 파일을 불러와 1개의 df로 만든다. 결과 : dataframes
    for csv_file_path in csv_file_paths:
        df_log = pd.read_csv(f"{url_log_folder_path}/{csv_file_path}", encoding=read_file_encoding)
        dataframes.append(df_log)

    merged_df = pd.concat(dataframes, ignore_index=True)  # 여러 개의 데이터프레임을 하나로 합침
    if subset is not None:  # subset이 None이면 실행하지 않는다
        merged_df = merged_df.drop_duplicates(subset=subset, keep='first')  # subset 칼럼에서 중복된 행을 제거 (첫 번째 행만 남김)

    print(merged_df.tail())

    # 3. df를 csv로 만든다
    merged_df.to_csv(f"{save_folder_path_}/{save_file_name}_{str_start_time}.csv", encoding=save_file_encoding,
                     index=False)
    print(f"[{len(csv_file_paths)}개의 파일을 {save_file_name}.csv 파일로 합쳤습니다]")
    print(f"총 데이터 개수 : {len(merged_df)}개")








    for gall_name in gall_name_list_:
        util.merge_csv_files(save_file_name=f"merged_url_crawling_log_{keyword}_{gall_name}",
                             read_folder_path_="./url/target_log",
                             save_folder_path_="./url/merged_log",
                             keyword=f"{gall_name}")

# df를 합치는 함수 정의
def merge_rows(df):
    # 'type' 열을 기준으로 그룹화하고 'count' 열의 값을 합산합니다.
    return df.groupby('type', as_index=False).sum()

# DataFrame 생성
data = {
    'type': ['url_crawler', 'url_crawler'],
    'count': [3, 5]
}
df = pd.DataFrame(data)

# 함수를 사용하여 합친 결과를 얻습니다.
merged_df = merge_rows(df)





util.merge_csv_files(keyword=keyword,
                     save_file_name=f"merged_url_crawling_log_{keyword}",
                     read_folder_path_="./url/merged_log",
                     save_folder_path_="./crawling_result",
                     save_file_encoding='ANSI')
