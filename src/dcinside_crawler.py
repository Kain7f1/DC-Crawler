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
# 기능 : 검색 조건의 dcinside 글 url 정보 받아오기
def crawl_url(gall_url, search_keyword, blacklist=None, whitelist=None, start_date=None, end_date=None):
    # [0-1. 기본값 세팅]
    crawling_start_time = datetime.now().replace(microsecond=0)    # 시작 시각 : 실행 시간을 잴 때 사용
    crawler_type = "url_crawler"    # 크롤러 타입
    community = "dcinside"          # 커뮤니티 이름
    black_count = 0                 # blacklist로 걸러진 글의 수
    str_start_time = str(crawling_start_time)[2:10].replace("-", "") + "_" + str(crawling_start_time)[11:].replace(":", "")
    # [0-2. default값 설정]
    url_rows, error_logs = [], []
    gall_name = ""
    error_log_file_path = f"./url/error_log/url_error_log_{search_keyword}_기본값세팅에러.csv"
    if blacklist is None:
        blacklist = []
    if whitelist is None:
        whitelist = []
    print(f"blacklist = {blacklist}")
    print(f"whitelist = {whitelist}")
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
        crawling_result_file_path = f"./url/crawling_result/url_crawling_result_{search_keyword}_{gall_name}_{str_start_time}.csv"  # 크롤링 결과 파일 이름
        crawling_log_file_path = f"./url/crawling_log/url_crawling_log_{search_keyword}_{gall_name}_{str_start_time}.csv"           # 크롤링 로그 파일 이름
        error_log_file_path = f"./url/error_log/url_error_log_{search_keyword}_{gall_name}_{str_start_time}.csv"                    # 에러 로그 파일 이름
    except Exception as e:
        print("[에러 발생 : 0. 기본값 세팅]", e)
        error_info = traceback.format_exc()
        error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
        cr.check_error_logs(error_logs, error_log_file_path)
        return

    # [1. url 크롤링]
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
        # [1-1.페이지 넘기면서 크롤링]
        for page in range(1, last_page+1):          # page = 1만 단위 검색결과 페이지
            element_list = []
            # [1-1-1. 검색결과 페이지 정보 가져오기 (1만 단위 검색결과)]
            try:
                search_result_url = f"{url_base}/board/lists/?id={gall_id}&page={page}&search_pos=-{search_pos}&s_type=search_subject_memo&s_keyword={search_keyword_unicode}"
                search_soup = cr.get_soup(search_result_url)        # soup (1만 단위 검색결과)
                element_list = cr.get_search_result(search_soup)    # element = 1줄 (글 한 개)
            except Exception as e:
                print("[에러 발생 : 글 한 개씩 정보 가져오기]", e)
                error_info = traceback.format_exc()
                error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
            # [1-1-2. 글 한 개씩 정보 가져오기]
            for element in element_list:
                try:
                    new_row, is_ignore, is_black = cr.get_url_row(element, search_info, blacklist, whitelist, start_date, end_date)
                    if is_ignore:    # blacklist의 단어가 있거나, 광고or공지글
                        if is_black:    # blacklist로 걸러지면 black_count +1
                            black_count += 1
                        continue     # 다음 element로 넘어간다
                    else:                          # 정상적이면
                        url_rows.append(new_row)   # url_rows에 크롤링한 정보 저장
                    print(f"[{search_pos} {page}/{last_page}] new_row : {new_row}")
                except Exception as e:
                    print("[에러 발생 : 글 한 개씩 정보 가져오기]", e)
                    error_info = traceback.format_exc()
                    error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])

    crawling_end_time = datetime.now().replace(microsecond=0)                                # 종료 시각 : 실행 시간을 잴 때 사용
    crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())     # 실행 시간 : 크롤링에 걸린 시간
    error_count = len(error_logs)   # 에러가 발생한 횟수
    row_count = len(url_rows)       # 크롤링된 row 개수

    if row_count > 0:   # 데이터가 0개면 저장안함
        # [2. url 크롤링 결과 저장 : .csv 파일]
        print(f"[{gall_name} : '{search_keyword}' 크롤링 결과]")
        print(f"[소요된 시간] {crawling_duration} 초")
        print(f"[수집한 정보] {row_count} 개")
        url_columns = ['community', 'gall_id', 'search_keyword', 'number', 'date_created', 'time_created', 'url', 'title', 'author', 'recommend']
        df_crawling_result = pd.DataFrame(url_rows, columns=url_columns)
        df_crawling_result.to_csv(crawling_result_file_path, encoding='utf-8', index=False)  # df의 내용을 csv 형식으로 저장합니다

        # [3. 크롤링 로그 저장 : .csv 파일]
        crawling_log_row = [[
            crawler_type, community, gall_name, row_count, crawling_duration, black_count, error_count,
            gall_id, gall_url, search_keyword, blacklist, whitelist, crawling_start_time, crawling_end_time
            ]]
        crawling_log_columns = [
            'crawler_type', 'community', 'gall_name', 'row_count', 'crawling_duration', 'black_count', 'error_count',
            'gall_id', 'gall_url', 'search_keyword', 'blacklist', 'whitelist', 'crawling_start_time', 'crawling_end_time'
            ]
        df_crawling_log = pd.DataFrame(crawling_log_row, columns=crawling_log_columns)
        df_crawling_log.to_csv(crawling_log_file_path, encoding='utf-8', index=False)  # df의 내용을 csv 형식으로 저장합니다
    else:
        print("수집된 데이터가 0건이므로, 파일을 생성하지 않습니다")

    # [4. 에러로그확인]
    cr.check_error_logs(error_logs, error_log_file_path)
    print("crawl_url() 함수가 정상적으로 종료되었습니다")
    return


#####################################
# 기능 : dcinside 글 url을 타고 들어가서 본문과 댓글 정보를 수집한다
def crawl_text(gall_url, search_keyword, blacklist=None, whitelist=None, start_date=None, end_date=None, chunk_size=100):
    # [0-1. 기본값 세팅]
    crawling_start_time = datetime.now().replace(microsecond=0)  # 시작 시각 : 실행 시간을 잴 때 사용
    crawler_type = "text_crawler"  # 크롤러 타입
    community = "dcinside"  # 커뮤니티 이름
    black_count = 0  # blacklist로 걸러진 글의 수
    str_start_time = (str(crawling_start_time)[2:10].replace("-", "")
                      + "_" + str(crawling_start_time)[11:].replace(":", ""))
    # [0-2. default값 설정]
    error_logs = []
    gall_name = ""
    error_log_file_path = f"./url/error_log/url_error_log_{search_keyword}_기본값세팅에러.csv"
    if blacklist is None:
        blacklist = []
    if whitelist is None:
        whitelist = []
    print(f"blacklist = {blacklist}")
    print(f"whitelist = {whitelist}")
    try:
        util.create_folder(f"./text/temp_crawling_result")  # 폴더 만들기 : temp_crawling_result
        util.create_folder(f"./text/crawling_result")       # 폴더 만들기 : crawling_result
        util.create_folder(f"./text/crawling_log")          # 폴더 만들기 : crawling_log
        util.create_folder(f"./text/error_log")             # 폴더 만들기 : error_log
        soup = cr.get_soup(gall_url)        # 갤러리 이름 받아오기 위한 soup 설정
        gall_id = cr.get_gall_id(gall_url)  # 갤러리 id
        gall_name = cr.get_gall_name(soup)  # 갤러리 이름
        url_file_path = util.find_file(f"{search_keyword}_{gall_name}", "./url/crawling_result")  # 키워드/갤러리이름 으로 파일을 검색한다
        if url_file_path is None:
            print("crawl_text()를 종료합니다")
            return
        url_file_path = f"./url/crawling_result/" + url_file_path
        done_index = cr.get_done_index(f"{search_keyword}_{gall_name}", f"./text/temp_crawling_result")    # 작업했던 마지막 파일의 번호
        crawling_result_file_name = \
            f"text_crawling_result_{search_keyword}_{gall_name}"  # 크롤링 결과 파일 이름
        crawling_log_file_path = \
            f"./text/crawling_log/text_crawling_log_{search_keyword}_{gall_name}_{str_start_time}.csv"  # 크롤링 로그
        error_log_file_path = \
            f"./text/error_log/text_error_log_{search_keyword}_{gall_name}_{str_start_time}.csv"  # 에러 로그
    except Exception as e:
        print("[에러 발생 : 0. 기본값 세팅]", e)
        error_info = traceback.format_exc()
        error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
        cr.check_error_logs(error_logs, error_log_file_path)
        return

    # [1. url.csv 파일 정보를 읽어와서, 크롤링]
    df_url = pd.read_csv(url_file_path, encoding='utf-8')
    url_row_count = len(df_url)     # url csv 파일 데이터 개수
    if url_row_count == 0:
        print("[crawl_text() 종료] url 파일에 저장된 데이터가 없습니다.")
        return
    print(f"[df_url을 불러왔습니다. 데이터 수 : {url_row_count}]")
    sub_dfs = util.split_df_into_sub_dfs(df_url, chunk_size=chunk_size)     # df를 chunk_size 단위로 쪼갬
    print(f"[데이터를 sub_df 단위로 쪼갰습니다. sub_df의 수 : {len(sub_dfs)}]")
    for sub_df_index in range(len(sub_dfs)):
        # [1-1. 작업했던 파일이 존재하면, 다음 것부터 시작한다]
        if sub_df_index <= done_index:
            continue
        sub_df = sub_dfs[sub_df_index]  # 작업할 단위 설정 : dub_df
        sub_df_data = []                # 데이터를 저장할 공간 : sub_df_data
        for index, url_row in sub_df.iterrows():
            # [1-1-a. sub_df에서, url_row 1개씩 읽어온다]
            print(f"[{sub_df_index * chunk_size + index + 1}/{url_row_count}] 본문 페이지 : {url_row['url']}")
            soup = cr.get_soup(url_row['url'])    # url을 Beatifulsoup를 사용하여 읽어온다
            if cr.is_deleted_page(soup):          # 글이 삭제되었는지 검사
                continue                          # 글이 삭제되었으면, 다음 row로 넘어갑니다
            print("{step 1} 본문 정보를 추가하겠습니다")
            new_row, is_ignore, is_black = cr.get_post_row(url_row, soup, blacklist, whitelist)  # 본문 정보 크롤링
            if is_ignore:
                print("{end} 무의미한 정보는 수집하지 않습니다 ")
                if is_black:    # blacklist로 걸러지면 black_count +1
                    black_count += 1
                continue        # 다음 element로 넘어간다
            else:
                sub_df_data.append(new_row)  # sub_df_data에 크롤링한 정보 저장
                print("{step 1} 본문 정보를 추가했습니다 : ", new_row[-1])
            # [1-1-b. 댓글 리스트를 가져온다]
            reply_list = cr.get_reply_list(url_row['url'])  # 댓글 리스트 soup
            print("{step 2} 댓글 리스트를 불러왔습니다")
            # [1-1-b-1. 댓글이 없으면 다음 글로 넘어감]
            if not reply_list:
                print("{end} 댓글이 존재하지 않습니다")
                continue
            # [1-1-b-2. 댓글이 있으면 댓글 정보를 가져온다]
            print("{step 3} 댓글 정보를 크롤링합니다")
            for reply in reply_list:
                try:
                    if cr.is_ignore_reply(reply):   # [무의미한 댓글 넘어가기]
                        continue
                    # [댓글 정보 가져오기]
                    new_row, is_ignore = cr.get_reply_row(url_row, reply, start_date, end_date)
                    if is_ignore:
                        continue
                    sub_df_data.append(new_row)     # sub_df_data에 new_row를 추가한다
                    print(f"[댓글을 추가했습니다] {new_row}")
                except Exception as e:
                    print(f"[댓글 크롤링 에러] {e}")
                    error_info = traceback.format_exc()
                    error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
                    cr.check_error_logs(error_logs, error_log_file_path)
                    continue
            print("{step 3 종료} 댓글 크롤링 완료하였습니다")
        # [1-2. sub_df 크롤링 결과를 csv 파일로 저장]
        try:
            # [임시파일 저장 : .csv 파일]
            print("[sub_df 크롤링 결과 임시파일을 저장합니다]")
            text_columns = ['community', 'gall_id', 'search_keyword', 'number',
                            'date_created', 'time_created', 'author', 'is_reply', 'text']
            df_temp_file = pd.DataFrame(sub_df_data, columns=text_columns)
            temp_file_index = "{:03}".format(sub_df_index)
            temp_file_path = (f"./text/temp_crawling_result/"
                              f"{temp_file_index}_temp_text_{search_keyword}_{gall_name}.csv")  # 임시 파일 경로
            df_temp_file.to_csv(temp_file_path, encoding='utf-8', index=False)    # 임시파일 저장
        except Exception as e:
            print('[sub_df 저장 에러] ', e)
            error_info = traceback.format_exc()
            error_logs.append([crawler_type, community, gall_name, search_keyword, error_info])
            cr.check_error_logs(error_logs, error_log_file_path)

    # [2-1. 임시 파일을 합쳐서 저장한다]
    print(f"임시파일을 {crawling_result_file_name}로 합치겠습니다")
    util.merge_csv_files(save_file_name=crawling_result_file_name, read_folder_path_="./text/temp_crawling_result",
                         save_folder_path_="./text/crawling_result", keyword=f"{search_keyword}_{gall_name}")
    crawling_end_time = datetime.now().replace(microsecond=0)                              # 종료 시각 : 실행 시간을 잴 때 사용
    crawling_duration = round((crawling_end_time - crawling_start_time).total_seconds())     # 실행 시간 : 크롤링에 걸린 시간
    error_count = len(error_logs)  # 에러가 발생한 횟수
    # [2-2. 임시파일 합쳤으면, 임시파일을 삭제한다]
    util.delete_files(folder_path="./text/temp_crawling_result", keyword=f"{search_keyword}_{gall_name}")

    # [2-3. 합친 파일을 불러온다]
    crawling_result_file = util.find_file(f"{search_keyword}_{gall_name}", "./text/crawling_result")
    df_crawling_result = pd.read_csv(f"./text/crawling_result/{crawling_result_file}", encoding='utf-8')
    row_count = len(df_crawling_result)  # 크롤링된 row 개수

    print(f"[{gall_name} : '{search_keyword}' 크롤링 결과]")
    print(f"[소요된 시간] {crawling_duration} 초")
    print(f"[수집한 정보] {row_count} 개")

    # [3. 크롤링 로그 저장 : .csv 파일]
    crawling_log_row = [[
        crawler_type, community, gall_name, row_count, crawling_duration, black_count, error_count,
        gall_id, gall_url, search_keyword, blacklist, whitelist, crawling_start_time, crawling_end_time
    ]]
    crawling_log_columns = [
        'crawler_type', 'community', 'gall_name', 'row_count', 'crawling_duration', 'black_count', 'error_count',
        'gall_id', 'gall_url', 'search_keyword', 'blacklist', 'whitelist', 'crawling_start_time', 'crawling_end_time'
    ]
    df_crawling_log = pd.DataFrame(crawling_log_row, columns=crawling_log_columns)
    df_crawling_log.to_csv(crawling_log_file_path, encoding='utf-8', index=False)  # df의 내용을 csv 형식으로 저장합니다

    # [4. 에러로그확인]
    cr.check_error_logs(error_logs, error_log_file_path)
    print("crawl_text() 함수가 정상적으로 종료되었습니다")
    return


##############################################
