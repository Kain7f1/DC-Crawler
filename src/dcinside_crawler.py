#############################
# Made by Hansol Lee
# 20230927
#############################
from datetime import datetime
import crawling_tool as cr
import utility_module as util
import pandas as pd
import traceback


##############################################
# 목적 : 디시인사이드 글 url 받아오기
# 입력값 : 입력 키워드(토스), 갤러리 id
# 리턴 : x
# 생성 파일 : url_dcinside_{gall_id}.csv
# columns = ['date', 'title', 'url', 'media']
def crawl_url(gall_url, search_keyword, blacklist, whitelist=None):
    # 0. 기본값 세팅
    crawling_start_time = datetime.now().replace(microsecond=0)    # 시작 시각 : 실행 시간을 잴 때 사용
    crawler_type = "url_crawler"    # 크롤러 타입
    community = "dcinside"          # 커뮤니티 이름
    black_count = 0                 # blacklist로 걸러진 글의 수
    # [default값 설정]
    url_rows, error_logs = [], []
    gall_name = ""
    error_log_file_path = f"./url/error_log/url_error_log_{search_keyword}_기본값세팅에러.csv"
    if whitelist is None:
        whitelist = []
    try:
        soup = cr.get_soup(gall_url)   # soup 설정
        gall_id = cr.get_gall_id(gall_url)      # 갤러리 id
        gall_name = cr.get_gall_name(soup)      # 갤러리 이름
        max_number = cr.get_max_number(soup)    # 검색결과 중, 가장 큰 글번호 10000단위로 올림한 값/10000
        url_base = cr.get_url_base(gall_url)     # url에서 "https" 부터 "board/" 이전까지의 부분 (major갤, minor갤, mini갤)
        search_keyword_unicode = util.convert_to_unicode(search_keyword)   # search_keyword를 유니코드로 변환
        search_info = {"community": community,              # 검색 정보/ 검색 조건.
                       "gall_id": gall_id,
                       "search_keyword": search_keyword}
        util.create_folder(f"./url/crawling_result")    # 폴더 만들기 : crawling_result
        util.create_folder(f"./url/crawling_log")       # 폴더 만들기 : crawling_log
        util.create_folder(f"./url/error_log")          # 폴더 만들기 : error_log
        crawling_result_file_path = f"./url/crawling_result/url_crawling_result_{search_keyword}_{gall_name}.csv"  # 크롤링 결과 파일 이름
        crawling_log_file_path = f"./url/crawling_log/url_crawling_log_{search_keyword}_{gall_name}.csv"           # 크롤링 로그 파일 이름
        error_log_file_path = f"./url/error_log/url_error_log_{search_keyword}_{gall_name}.csv"                    # 에러 로그 파일 이름
    except Exception as e:
        print("[에러 발생 : 0. 기본값 세팅]", e)
        error_info = traceback.format_exc()
        error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
        cr.check_error_logs(error_logs, error_log_file_path)
        return

    # 1. url 크롤링
    for search_pos in range(max_number, 0, -10000):
        # [1만 단위 검색결과의 last_page 받아오기]
        last_page = 1
        try:
            temp_url = f"{url_base}/board/lists/?id={gall_id}&page=1&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={search_keyword_unicode}"
            print(f"[{search_keyword}의 검색 결과 / 범위 : {search_pos}~{search_pos-10000}] {temp_url}")
            temp_soup = cr.get_soup(temp_url)           # soup 받아오기
            last_page = cr.get_last_page(temp_soup)     # 1만 단위 검색결과의 마지막 페이지
        except Exception as e:
            print("[에러 발생 : 글 한 개씩 정보 가져오기]", e)
            error_info = traceback.format_exc()
            error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
        # [페이지 넘기면서 크롤링]
        for page in range(1, last_page+1):          # page = 1만 단위 검색결과 페이지
            element_list = []
            # [1만 단위 검색결과 페이지]
            try:
                search_result_url = f"{url_base}/board/lists/?id={gall_id}&page={page}&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={search_keyword_unicode}"
                search_soup = cr.get_soup(search_result_url)        # soup (1만 단위 검색결과)
                element_list = cr.get_search_result(search_soup)    # element = 1줄 (글 한 개)
            except Exception as e:
                print("[에러 발생 : 글 한 개씩 정보 가져오기]", e)
                error_info = traceback.format_exc()
                error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
            # [글 한 개씩 정보 가져오기]
            for element in element_list:
                try:
                    is_ignore, new_row = cr.get_url_row(element, search_info, blacklist, whitelist)
                    if is_ignore:    # blacklist의 단어가 있거나, 광고or공지 글이면
                        black_count += 1
                        continue     # 다음 element로 넘어간다
                    else:                          # 정상적이면
                        url_rows.append(new_row)   # df_data에 크롤링한 정보 저장
                    print(f"[{search_pos} {page}/{last_page}] new_row : {new_row}")
                except Exception as e:
                    print("[에러 발생 : 글 한 개씩 정보 가져오기]", e)
                    error_info = traceback.format_exc()
                    error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])

    crawling_end_time = datetime.now().replace(microsecond=0)                              # 종료 시각 : 실행 시간을 잴 때 사용
    crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())     # 실행 시간 : 크롤링에 걸린 시간
    error_count = len(error_logs)                                    # 에러가 발생한 횟수
    row_count = len(url_rows)                                    # 크롤링된 row 개수

    # 2. url 크롤링 결과 저장 : .csv 파일
    print(f"[{gall_name} : '{search_keyword}' 크롤링 결과]")
    print(f"[걸린 시간] {crawling_duration} 초")
    print(f"[모은 정보] {row_count} 개")
    url_columns = ['community', 'gall_id', 'search_keyword', 'number', 'date', 'time_', 'url', 'title', 'author', 'recommend']
    df_crawling_result = pd.DataFrame(url_rows, columns=url_columns)
    df_crawling_result.to_csv(crawling_result_file_path, encoding='utf-8', index=False)  # df의 내용을 csv 형식으로 저장합니다

    # 3. 크롤링 로그 저장 : .csv 파일
    crawling_log_row = [[crawler_type, community, gall_id, gall_name, gall_url, search_keyword,
                         blacklist, whitelist, crawling_start_time, crawling_end_time,
                         black_count, error_count, row_count, crawling_duration
                         ]]
    crawling_log_columns = ['crawler_type', 'community', 'gall_id', 'gall_name', 'gall_url', 'search_keyword',
                            'blacklist', 'whitelist', 'crawling_start_time', 'crawling_end_time',
                            'black_count', 'error_count', 'row_count', 'crawling_duration']

    df_crawling_log = pd.DataFrame(crawling_log_row, columns=crawling_log_columns)
    df_crawling_log.to_csv(crawling_log_file_path, encoding='utf-8', index=False)  # df의 내용을 csv 형식으로 저장합니다

    # 4. 에러로그확인
    cr.check_error_logs(error_logs, error_log_file_path)
    print("crawl_url() 함수가 정상적으로 종료되었습니다")
    return


#####################################
# merge_url_files()
# 기능 : 2개 이상의 키워드로 crawl_url()한 url 파일들을 중복제거하여 하나로 합친다
def merge_url_files(result_file_name, folder_path_='./'):
    dataframes = []     # df들을 저장할 리스트

    # 1. 폴더 내의 파일을 검색한다
    csv_file_paths = util.read_file_paths(folder_path_, endswith='.csv')  # 폴더 내의 .csv로 끝나는 파일들 전부 검색
    print(f'[{len(csv_file_paths)}개의 파일을 합치겠습니다]')
    for csv_file_path in csv_file_paths:
        print(csv_file_path)            # 합쳐질 파일들 이름 출력

    # 2. df 합치기
    for csv_file_path in csv_file_paths:
        df_content = pd.read_csv(f"{folder_path_}/{csv_file_path}", encoding='utf-8')
        dataframes.append(df_content)
    merged_df = pd.concat(dataframes, ignore_index=True)    # 여러 개의 데이터프레임을 하나로 합침
    merged_df_unique = merged_df.drop_duplicates(subset='number', keep='first')     # 'number' 칼럼에서 중복된 행을 제거 (첫 번째 행만 남김)

    print(merged_df_unique.tail())

    # 3. df를 csv로 만든다
    result_folder_path = util.create_folder(f"{folder_path_}/{result_file_name}")
    merged_df_unique.to_csv(f"{result_folder_path}/{result_file_name}.csv", encoding='utf-8', index=False)
    print(f"[{len(csv_file_paths)}개의 파일을 {result_file_name}.csv 파일로 합쳤습니다]")
    print(f"총 데이터 개수 : {len(merged_df_unique)}개")


#####################################
# get_content()
# 목적 : url.csv를 읽어오고, 각 페이지의 정보를 추출하여 저장한다
# 입력값 : media
# 리턴값 : 없음
# 생성 파일 : content_dcinside_toss.csv
# columns = ['date', 'title', 'url', 'media', 'content', 'is_comment']
#################################
# [함수 진행]
# 1) url.csv를 df로 읽어옴
# 2-a) df에서 한 row 읽어옴
# 2-b) 본문 정보 row를 sub_df_data에 추가
# 2-c) 댓글들 정보 row를 sub_df_data에 추가
# 3-a) 다 끝났으면 다음 row 읽어옴
# 3-b) 2,3 반복
# 4) 끝나면 파일로 저장
# 5) 에러로그 체크 및 저장
#################################
@util.timer_decorator
def crawl_text(gall_url, keyword, blacklist, whitelist=None, chunk_size=1000):
    crawling_start_time = datetime.now()    # 실행 시간을 잴 때 사용
    crawler_type = "url_crawler"
    community = "dcinside"              # 커뮤니티
    if whitelist is None:
        whitelist = []
    gall_id = cr.get_gall_id(gall_url)              # 갤 id
    url_folder_path = f"./url/{keyword}"            # 읽어올 url 폴더 경로 설정
    content_folder_path = f"./content/{keyword}"    # 저장할 content 폴더 경로 설정
    util.create_folder(content_folder_path)         # 저장할 content 폴더 만들기
    error_log = []                                  # 에러 로그 저장
    url_file_name = f"url_{keyword}_{gall_id}"      # url csv 파일 이름
    content_file_name = f"content_{keyword}_{gall_id}"        # content 파일 이름
    done_index = util.get_last_number_in_folder(content_folder_path)    # 마지막 파일 번호

    # 1) url.csv를 df로 읽어옴
    df_url = util.read_csv_file(f"{url_file_name}.csv", url_folder_path)
    row_count = len(df_url)     # url csv 파일 데이터 개수
    sub_dfs = util.split_df_into_sub_dfs(df_url, chunk_size=chunk_size)     # df를 chunk_size 단위로 쪼갬
    for sub_df_index in range(len(sub_dfs)):
        if sub_df_index <= done_index:   # 작업했던 파일이 존재하면
            continue                    # 넘어갑니다
        sub_df = sub_dfs[sub_df_index]
        sub_df_data = []  # 데이터 리스트 ['date', 'title', 'url', 'media', 'content', 'is_comment']
        for index, url_row in sub_df.iterrows():
            # sub_df에서 한 url_row씩 읽어옴
            title = url_row['title']
            url = url_row['url']
            print(f"[{sub_df_index * chunk_size + index + 1}/{row_count}] 본문 페이지 : {url}")
            soup = cr.get_soup(url)    # url을 Beatifulsoup를 사용하여 읽어온다
            if cr.is_deleted_page(soup):        # 글이 삭제되었는지 검사
                continue    # 글이 삭제되었으면, 다음 row로 넘어갑니다
            # {step 1} 본문 정보 row를 sub_df_data에 추가
            print("{step 1 시작} 본문 정보를 추가하겠습니다")
            new_row = cr.get_new_row_from_main_content(url_row, soup)  # 본문 정보를 추가
            if util.contains_any_from_list(new_row[-2], whitelist):    # whitelist의 단어가 있으면
                print("[본문 content에 whitelist에 해당하는 단어 발견]")
                pass
            elif util.contains_any_from_list(new_row[-2], blacklist):  # blacklist의 단어가 있으면
                print("{step 1~3 종료} 본문 content에 blacklist에 해당하는 단어 발견 : ", new_row[-2])
                continue    # blacklist의 단어가 있으면, 다음 row로 넘어갑니다
            sub_df_data.append(new_row)     # sub_df_data에 new_row를 추가한다
            print("{step 1 종료} 본문을 추가했습니다", new_row[0], new_row[-2])

            # {step 2} 댓글들 정보들을 불러오겠습니다
            # new_row 형식 : ['date', 'title', 'url', 'media', 'content', 'is_comment']
            print("{step 2 시작} 댓글 정보들을 불러오겠습니다")
            reply_list = cr.get_reply_list(url)  # 댓글 리스트 soup
            print("{step 2 종료} 댓글 정보들을 불러왔습니다")

            # 댓글이 없으면 다음 글로 넘어감
            if not reply_list:
                print("{step 3 종료} 댓글이 없습니다. 다음 url_row로 넘어갑니다")
                continue
            # 댓글이 있으면 댓글 정보를 가져온다
            print("{step 3 시작} 댓글이 존재합니다. 댓글 정보를 크롤링 하겠습니다")
            for reply in reply_list:
                try:
                    # 필요없는 항목 넘어가기
                    if cr.is_ignore_reply(reply):
                        continue
                    # 댓글 정보 가져오기 : date, content
                    date = cr.get_reply_date(reply)
                    content = reply.find("p", {"class": "usertxt ub-word"}).text  # 댓글 내용 추출
                    content = util.preprocess_content_dc(content)    # 전처리
                    new_row = [date, title, url, gall_id, content, 1]  # new_row에 정보를 채워둔다
                    sub_df_data.append(new_row)                        # sub_df_data에 new_row를 추가한다
                    print(f"[댓글을 추가했습니다] {new_row}")
                except Exception as e:
                    status = "[{step 3} 댓글 정보를 크롤링]"
                    print(f'[ERROR][index : {index}]{status}[error message : {e}]')
                    error_log.append([index, status, e, title, url])
                    continue
            print("{step 3 종료} 댓글 크롤링 완료하였습니다")
        # sub_df 크롤링 결과를 csv 파일로 저장
        try:
            print(f"[{len(sub_df_data)}개의 content 정보가 저장되었습니다]")
            print(f"[갤러리 주소 : {gall_url}]")
            df_result = pd.DataFrame(sub_df_data, columns=['date', 'title', 'url', 'media', 'content', 'is_comment'])
            util.save_csv_file(df_result, f"{content_file_name}_{sub_df_index}.csv", content_folder_path)
        except Exception as e:
            print('[에러 발생. status : 결과 csv 파일로 저장] ', e)

    # sub_dfs를 합친다
    util.combine_csv_file(content_file_name, content_folder_path)

    crawling_end_time = datetime.now()
    crawling_duration = crawling_end_time - crawling_start_time

    # 에러 로그 체크, 저장
    try:
        cr.check_error_logs(error_log, "", content_folder_path)
    except Exception as e:
        print('[에러 발생. status : 에러 로그 체크] ', e)


##############################################
