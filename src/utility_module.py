import pandas as pd
import os
import re
import time


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
        print("[폴더가 이미 존재합니다]")
    else:
        os.makedirs(folder_path_)
        print(f"[폴더 : {folder_path_}를 만들었습니다]")
    print("[create_folder()를 종료합니다]")
    return folder_path_


#####################################
# read_file_paths()
# 입력값 : folder_path_, endswith (파일이름의 검색조건 : 파일명의 끝)
# 기능 : 폴더 내의 파일들 이름을 읽어서, 파일 이름들 리스트를 가져오는 함수
def read_file_paths(folder_path_='./', endswith='.csv'):
    file_paths = []
    print(f"[{folder_path_} 내의 파일을 탐색합니다. 검색조건 : endswith={endswith}]")
    for file_path in os.listdir(folder_path_):      # 폴더 내의 모든 파일을 검색한다
        if file_path.endswith(endswith):    # endswith 조건에 부합하면
            file_paths.append(file_path)    # file_paths 에 추가한다
    for file_path in file_paths:
        print(file_path)            # 검색한 파일 경로를 출력한다.

    return file_paths


#####################################
# 기능 : 마지막 숫자를 리턴하는 함수
# 입력값 : 문자열
# 리턴값 : 마지막 숫자(int), 숫자가 없으면 None
def get_last_number_from_string(str_):
    match = re.findall(r'\d+', str_)
    if match:
        return int(match[-1])
    else:
        return None


#####################################
# 기능 : 폴더 내 마지막 파일의 숫자를 가져오는 함수
def get_last_number_in_folder(folder_path_='./'):
    file_name_list = read_file_paths(folder_path_, endswith='.csv')  # 폴더 내 파일들 이름 읽어온다
    if len(file_name_list) == 0:    # 폴더 내에 endswith='.csv'인 파일이 없으면
        print('[폴더 내에 파일이 없습니다 : get_last_number_in_folder()]')
        return -1
    last_file_name = file_name_list[-1]   # 마지막 파일 이름
    print("last_file_name", last_file_name)
    match = re.findall(r'\d+', last_file_name)
    if match:
        return int(match[-1])
    else:                        # 마지막 파일 이름에 숫자가 없으면
        print('[마지막 파일 이름에 숫자가 없습니다 : get_last_number_in_folder()]')
        return -1


#####################################
# read_file()
# 기능 : .csv의 내용을 읽어옴
# 리턴값 : df 형식의 데이터
def read_csv_file(file_path, folder_path_='./'):
    combined_path = os.path.join(folder_path_, file_path)        # os.path.join()을 사용하여 두 경로를 합칩니다.
    return pd.read_csv(combined_path, encoding='utf-8')

#
# #####################################
# # save_csv_file()
# # 기능 : df의 내용을 파일로 저장한다
# def save_csv_file(df, file_path, folder_path_='./'):
#     combined_path = os.path.join(folder_path_, file_path)        # os.path.join()을 사용하여 두 경로를 합칩니다.
#     df.to_csv(combined_path, encoding='utf-8', index=False)     # df의 내용을 csv 형식으로 저장합니다


#####################################
# combine_csv_file()
# 기능 : df형식의 데이터가 저장되어있는 .csv 파일들을 하나로 합친다
def combine_csv_file(result_file_name, folder_path_='./'):
    csv_file_paths = read_file_paths(folder_path_, endswith='.csv')   # .csv로 끝나는 파일들을 전부 검색한다
    dataframes = []

    # 1. 잘 불러왔는지 확인하기
    print(f'[{len(csv_file_paths)}개의 파일을 합치겠습니다]')
    for csv_file_path in csv_file_paths:
        print(csv_file_path)

    # 2. df 합치기
    for csv_file_path in csv_file_paths:
        df_content = read_csv_file(file_path=csv_file_path, folder_path_=folder_path_)
        dataframes.append(df_content)

    merged_df = pd.concat(dataframes)
    # merged_df.drop_duplicates(subset='url', keep='first', inplace=True)  # 중복 제거 옵션
    merged_df = merged_df.reset_index(drop=True)
    print(merged_df.tail())

    # 3. df를 csv로 만든다
    result_folder_path = create_folder(f"{folder_path_}/{result_file_name}")
    merged_df.to_csv(f"{result_folder_path}/{result_file_name}.csv", encoding='utf-8', index=False)
    print(f"[{len(csv_file_paths)}개의 파일을 {result_file_name}.csv 파일로 합쳤습니다]")
    print(f"총 데이터 개수 : {len(merged_df)}개")


#####################################
# preprocess_content_dc()
# 전처리 함수 : dcinside
def preprocess_content_dc(text):
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


#########################################################################################################
# 한국어인지 검사하는 함수
def is_korean(s):
    return bool(re.fullmatch("[\u3131-\u3163\uAC00-\uD7A3]+", s))


# 불용어를 지운다
def remove_stopword(keyword):
    # 파일 열기
    folder_path = f'./{keyword}'
    read_file_path = f'{keyword}_content_tokenized.csv'
    result_file_path = f"{keyword}_content_tokenized_removed_stopwords.csv"
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        # 라인별로 읽어 리스트로 저장
        stopwords = file.readlines()
    stopwords = [word.strip() for word in stopwords]
    print('stopwords.txt 를 불러왔습니다')

    df = read_csv_file(folder_path, read_file_path)
    print(f'{read_file_path} 를 불러왔습니다')
    for stopword in stopwords:
        df['content'] = df['content'].str.replace(f'\\b{stopword} \\b', '', regex=True)
    print('stopwords를 지웠습니다')

    df.to_csv(f"{folder_path}/{result_file_path}", encoding='utf-8', index=False)

    print(f'{keyword}_removed_stopwords.csv 파일을 저장했습니다')


def dropna_and_save(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    df.dropna(inplace=True)
    df.to_csv(file_path, encoding='utf-8', index=False)
    