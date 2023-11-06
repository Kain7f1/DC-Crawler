import pandas as pd
import os
import re
import time
from datetime import datetime


#####################################
# 기능 : 함수의 실행 시간을 재는 데코레이터
# 사용법 : @util.timer_decorator 를 함수 정의할 때 함수명 윗줄에 적는다
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} 함수의 실행 시간은 {elapsed_time:.2f} 초 입니다")
        return result
    return wrapper


#####################################
# 기능 : 폴더를 생성한다
# 입력값 : 파일 경로(이름)
def create_folder(folder_path_='./'):
    # 폴더가 존재하지 않는 경우, 폴더 생성
    if os.path.exists(folder_path_):
        print(f"[{folder_path_} 폴더가 이미 존재합니다]")
    else:
        os.makedirs(folder_path_)
        print(f"[폴더 : {folder_path_}를 만들었습니다]")
    return folder_path_


#####################################
# read_files()
# 입력값 : folder_path_, endswith (파일이름의 검색조건 : 파일명의 끝)
# 기능 : 폴더 내의 파일들 이름을 읽어서, 파일 이름들 리스트를 가져오는 함수
def read_files(folder_path_='./', keyword=None, endswith='.csv'):
    file_list = []
    print(f"[{folder_path_} 내의 파일을 탐색합니다. 검색조건 : endswith={endswith}]")
    for target_file in os.listdir(folder_path_):      # 폴더 내의 모든 파일을 검색한다
        if target_file.endswith(endswith):    # endswith 조건에 부합하면
            if keyword is None:     # 키워드 조건이 없으면
                file_list.append(target_file)    # file_paths 에 추가한다
            else:    # 키워드 조건이 있으면
                if keyword in target_file:
                    file_list.append(target_file)  # file_paths 에 추가한다
    for index, found_file in enumerate(file_list):
        print(f"* File {index+1} * {found_file}")            # 검색한 파일 경로를 출력한다.

    return file_list


#####################################
# merge_csv_files()
# 기능 : .csv 파일들을 하나로 합친다
def merge_csv_files(save_file_name, read_folder_path_='./', save_folder_path_='./', keyword=None, subset=None, read_file_encoding='utf-8', save_file_encoding='utf-8'):
    create_folder(save_folder_path_)
    start_time = datetime.now().replace(microsecond=0)
    str_start_time = str(start_time)[2:10].replace("-", "") + "_" + str(start_time)[11:].replace(":", "")
    dataframes = []     # df들을 저장할 리스트

    # 1. 폴더 내의 파일을 검색한다
    csv_file_paths = read_files(read_folder_path_, keyword=keyword, endswith='.csv')  # 폴더 내의 .csv로 끝나는 파일들 전부 검색
    print(f'[{len(csv_file_paths)}개의 파일을 합치겠습니다]')
    for csv_file_path in csv_file_paths:
        print(csv_file_path)            # 합쳐질 파일들 이름 출력

    # 2. df 합치기
    for csv_file_path in csv_file_paths:
        df_content = pd.read_csv(f"{read_folder_path_}/{csv_file_path}", encoding=read_file_encoding)
        dataframes.append(df_content)
    merged_df = pd.concat(dataframes, ignore_index=True)    # 여러 개의 데이터프레임을 하나로 합침
    if subset is not None:  # subset이 None이면 실행하지 않는다
        merged_df = merged_df.drop_duplicates(subset=subset, keep='first')     # subset 칼럼에서 중복된 행을 제거 (첫 번째 행만 남김)

    print(merged_df.tail())

    # 3. df를 csv로 만든다
    merged_df.to_csv(f"{save_folder_path_}/{save_file_name}_{str_start_time}.csv", encoding=save_file_encoding, index=False)
    print(f"[{len(csv_file_paths)}개의 파일을 {save_file_name}.csv 파일로 합쳤습니다]")
    print(f"총 데이터 개수 : {len(merged_df)}개")


####################################
# 기능 : keyword 조건에 맞는 폴더 내 파일들을 삭제한다
def delete_files(folder_path, keyword=None):
    file_list = read_files(folder_path, keyword=keyword)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[파일을 삭제하였습니다] {file_path}")
        else:
            print(f"File not found: {file_path}")


#####################################
# 전처리 함수 : dcinside
def preprocess_text_dc(text):
    # 바꿀 것들 리스트
    replacements = {
        '\n': ' ',
        '\t': ' ',
        ',': ' ',
        '- dc official App': '',
        '- dc App': ''
    }
    for old, new in replacements.items():
        text = text.replace(old, new)   # replacements의 전자를 후자로 교체함
    result = text.strip()               # 공백제거
    if len(result) == 0:
        return "_"      # 널값이면 "_"을 리턴한다
    else:
        return result   # 전처리 결과값 리턴


##################################################
# 기능 : 입력한 문자열에, list의 원소가 포함되어 있으면 True, 아니면 False를 리턴하는 함수
def contains_any_from_list(str_, list_):
    for item in list_:
        if item in str_:
            return True
    return False


##########################################
# 기능 : 한글 문자열을 유니코드 UTF-8로 인코딩하여 반환합니다
# 입력 예시 : '에스엠'
# 리턴값 예시 : '.EC.97.90.EC.8A.A4.EC.97.A0'
def convert_to_unicode(input_str):
    return '.' + '.'.join(['{:02X}'.format(byte) for byte in input_str.encode('utf-8')])


##########################################
# split_rows_into_chunks()
# 기능 : row를 chunk_size단위로 끊은 리스트를 반환하는 함수
# 리턴값 : eX) row 개수가 2345면, [[0,999], [1000, 1999], [2000, 2344]]
def split_rows_into_chunks(row_count, chunk_size=1000):
    # 빈 리스트 초기화
    chunks = []

    # 시작과 끝 인덱스를 설정하여 리스트에 추가
    start_idx = 0
    while start_idx < row_count:
        end_idx = start_idx + chunk_size - 1
        if end_idx >= row_count:
            end_idx = row_count - 1
        chunks.append([start_idx, end_idx])
        start_idx += chunk_size

    return chunks


#########################################
# 기능 : DataFrame을 chunk_size 단위로 잘라서, 잘려진 DataFrame의 리스트를 반환하는 함수
# 입력값 : 자를 데이터프레임
# 리턴값 : 잘라진 df의 리스트
def split_df_into_sub_dfs(df, chunk_size=1000):
    row_count = len(df)  # row 개수 확인
    chunks = split_rows_into_chunks(row_count, chunk_size)  # chunk로 나눌 구간 생성

    # 각 chunk에 대해 DataFrame을 잘라서 리스트에 저장
    sub_dfs = []
    for chunk in chunks:
        start, end = chunk
        sub_df = df.iloc[start:end + 1]  # 해당 범위의 데이터를 가져옴
        sub_df = sub_df.reset_index(drop=True)
        sub_dfs.append(sub_df)

    return sub_dfs


########################################
# find_file()
# 기능 : 키워드를 조건으로, 폴더 내의 파일을 1개 찾아내어 리턴
# 리턴값 : 예를들어 "text_기아_캠퍼스개미갤러리.csv" 라는 문자열을 리턴한다
def find_file(keyword,  folder_path_='./'):
    read_file_list = read_files(folder_path_, keyword=keyword)
    file_list = []
    for target_file in read_file_list:
        if keyword in target_file and target_file.endswith('.csv'):
            file_list.append(target_file)
    if len(file_list) == 0:
        print("[파일을 발견하지 못했습니다]")
        return None
    else:
        found_file = file_list[-1]
        print(f"[파일을 발견하였습니다] {found_file}")
        return found_file


#########################################################################################################
# 한국어인지 검사하는 함수
def is_korean(s):
    return bool(re.fullmatch("[\u3131-\u3163\uAC00-\uD7A3]+", s))


#######################################
# url~text 크롤링 결과와 로그 파일을 합쳐 4개의 파일로 만든다
def merge_crawling_results(keyword):
    merge_csv_files(keyword=keyword, save_file_name=f"merged_url_crawling_result_{keyword}",
                    read_folder_path_="./url/crawling_result", save_folder_path_="./crawling_result")
    merge_csv_files(keyword=keyword, save_file_name=f"merged_url_crawling_log_{keyword}",
                    read_folder_path_="./url/crawling_log", save_folder_path_="./crawling_result", save_file_encoding='ANSI')
    merge_csv_files(keyword=keyword, save_file_name=f"merged_text_crawling_result_{keyword}",
                    read_folder_path_="./text/crawling_result", save_folder_path_="./crawling_result")
    merge_csv_files(keyword=keyword, save_file_name=f"merged_text_crawling_log_{keyword}",
                    read_folder_path_="./text/crawling_log", save_folder_path_="./crawling_result", save_file_encoding='ANSI')


#######################################
# 기능 : 특정 키워드(delete_keyword)가 포함된 row를 제거한 후 파일로 저장한다
# 전제 : "target" 폴더에 적용할 파일을 올려둔다
def delete_rows(delete_keyword, column='text', folder_path="./target"):
    result_folder_path = create_folder(f"{folder_path}/result_files")
    file_list = read_files(folder_path_=folder_path)

    for file in file_list:
        file_path = f"{folder_path}/{file}"
        df = pd.read_csv(file_path, encoding='utf-8')   # 파일 읽어오기
        len_df_before = len(df)                         # 지우기 전 row 개수
        df_new = df[~df[column].str.contains(delete_keyword)]   # delete_keyword 가 포함된 row 제거하여 반환
        len_df_after = len(df_new)                      # 지운 후 row 개수
        len_diff = len_df_before - len_df_after         # 지워진 row 수
        print(f"{len_diff} 개의 row가 삭제되었습니다. delete_keyword = {delete_keyword}")
        df_new.to_csv(f"{result_folder_path}/deleted_rows_{file}", encoding="utf-8", index=False)  # 파일로 저장
        print(f"{len_df_after} 개의 row가 파일로 저장되었습니다")
