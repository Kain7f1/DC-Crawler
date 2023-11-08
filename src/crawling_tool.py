import re
import os
import time
import requests
from datetime import datetime
import pandas as pd
import utility_module as util
from bs4 import BeautifulSoup
from selenium import webdriver


#############################################################################
#                                 << 설정값 >>
# dcinside 헤더 :  dcinside 봇 차단을 위한 헤더 설정
headers_dc = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "sec-ch-ua-mobile": "?0",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }

# 목적에 맞는 헤더를 설정한다
headers = headers_dc


###############################################################################
#                                 << 함수들 >>                                 #
###############################################################################
# get_driver()
# 사용 전제 조건 : Users 폴더에 버전에 맞는 chromedriver.exe를 다운받아주세요
# 기능 : driver를 반환합니다
# 리턴값 : driver
# 사용법 : driver = get_driver() 쓰고 driver.get(url) 처럼 사용합니다
def get_driver():
    CHROME_DRIVER_PATH = "C:/Users/chromedriver.exe"    # (절대경로) Users 폴더에 chromedriver.exe를 설치했음
    options = webdriver.ChromeOptions()                 # 옵션 선언
    # [옵션 설정]
    # options.add_argument("--start-maximized")         # 창이 최대화 되도록 열리게 한다.
    options.add_argument("--headless")                  # 창이 없이 크롬이 실행이 되도록 만든다
    options.add_argument("disable-infobars")            # 안내바가 없이 열리게 한다.
    options.add_argument("disable-gpu")                 # 크롤링 실행시 GPU를 사용하지 않게 한다.
    options.add_argument("--disable-dev-shm-usage")     # 공유메모리를 사용하지 않는다
    options.add_argument("--blink-settings=imagesEnabled=false")    # 이미지 로딩 비활성화
    options.add_argument('--disk-cache-dir=/path/to/cache-dir')     # 캐시 사용 활성화
    options.page_load_strategy = 'none'             # 전체 페이지가 완전히 로드되기를 기다리지 않고 다음 작업을 수행 (중요)
    options.add_argument('--log-level=3')           # 웹 소켓을 통한 로그 메시지 비활성화
    options.add_argument('--no-sandbox')            # 브라우저 프로파일링 비활성화
    options.add_argument('--disable-plugins')       # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-extensions')    # 다양한 플러그인 및 기능 비활성화
    options.add_argument('--disable-sync')          # 다양한 플러그인 및 기능 비활성화
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    return driver


#############################################################################
# get_soup()
# 기능 : url을 받아 requests를 사용하여 soup를 리턴하는 함수입니다
# 특징 : 오류발생 시 재귀하기 때문에, 성공적으로 soup를 받아올 수 있습니다.
def get_soup(url, time_sleep=0, max_retries=600):
    try:
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_soup()]")
            return None
        with requests.Session() as session:
            response = session.get(url, headers=headers)
            time.sleep(time_sleep)
        soup = BeautifulSoup(response.text, "html.parser")
        if len(soup) == 0:  # 불러오는데 실패하면
            print(f"[soup 로딩 실패, 반복] [get_soup(time_sleep=1)]")
            soup = get_soup(url, 1)
    except Exception as e:
        print(f"[오류 발생, 반복] [get_soup(time_sleep=1)] ", e)
        soup = get_soup(url, 1, max_retries-1)
    return soup


#####################################
# 기능 : 에러 로그를 검사하고, 에러가 있으면 csv 파일을 만든다
def check_error_logs(error_logs, file_path_='./'):
    # error 발생 했는지 확인
    max_print_count = 5
    if len(error_logs) > 0:                             # 에러 로그가 존재하면
        print("[에러 발생 로그 입니다]")
        for index, error_log in enumerate(error_logs):  # 에러 로그를 출력한다
            print(f"[Index {index}] {error_log[-1]}")
            if index >= max_print_count:                # 사용자에게 보여주기 위해 출력하는 용도이므로, 조금만 출력
                break
        error_log_columns = ['crawler_type', 'community', 'gall_name', 'search_keyword', 'error_info']
        df_error_logs = pd.DataFrame(error_logs, columns=error_log_columns)        # df 생성 후 .csv 파일로 저장
        df_error_logs.to_csv(file_path_, encoding='ANSI', index=False)
        print(f"[총 {len(error_logs)}개의 에러 로그가 파일로 저장되었습니다]")
    else:                                               # 에러가 존재하지 않으면, 종료
        print("[에러가 없었습니다]")
    return len(error_logs)


#############################
# get_gall_name()
# 기능 : 갤러리 이름을 리턴한다 ex) 식물갤러리 -> "식물"
def get_gall_name(soup):
    gall_name = soup.select_one("div.page_head div.fl").get_text(strip=True)
    pattern = r"(갤러리)[미니,마이너]*"
    gall_name = re.sub(pattern, r"\1", gall_name)   # "갤러리" 이후의 부분을 없애준다
    return gall_name.replace(" ", "")[:-3]        # 공백, "갤러리" 제거하고 리턴


#############################
# is_deleted_url()
# 기능 : url을 받아, 글이 삭제되었는지 아닌지 확인합니다
# 입력값 : 글 url
# 리턴값 : 글이 삭제되었으면 True, 글이 온전하면 False
def is_deleted_page(soup):
    try:
        defer = soup.select_one('script')['defer']
        return False
    except Exception as e:
        print("[삭제된 페이지입니다] ", e)
        return True


###############################
# get_search_result()
# 기능 : 검색결과 페이지 정보를 불러온다
# 리턴값 : 검색결과의 글 리스트
def get_search_result(soup, time_sleep=0):
    try:
        element_list = soup.select("table.gall_list tr.ub-content")  # 한 페이지 전체 글 리스트
        if len(element_list) == 0:  # 검색 결과는 광고글를 포함해서 최소 1개 이상이어야 한다. 없으면 다시 돌림
            print("[검색 실패, 반복] [get_search_result()]")
            element_list = get_search_result(soup, time_sleep+1)
    except Exception as e:
        print("[오류 발생, 반복] [get_search_result()] ", e)
        element_list = get_search_result(soup, time_sleep+1)
    return element_list


###############################
# get_max_content_num()
# 기능 : 검색결과 중 가장 큰 글번호를 구하여 리턴한다
# 리턴값 : max_content_num
def get_max_number(soup):
    box = soup.select("div.gall_listwrap tr.ub-content")  # 글만 있는 box
    # 메이저 / 마이너&미니 갤러리는 max_content_num을 긁어올 부분이 다르다
    if box[0].find('td', class_='gall_subject'):
        classification = 'gall_subject'
    else:
        classification = 'gall_num'

    print("classification :", classification)
    first_content_num = ''
    ignore_list = ["설문", "AD", "공지", "이슈"]  # 무시할 리스트. 공지나 광고 같은거 있으면 패스
    for content in box:
        content_num = content.find('td', class_=classification).get_text()
        # ignore_list에 있으면 제외
        if content_num in ignore_list:
            continue
        # ignore_list 제외한 가장 첫번째 글
        first_content_num = content.select_one("td.gall_num").get_text()

    max_content_num = int(int(first_content_num) / 10000 + 1) * 10000   # 1만단위로 변환
    return max_content_num


#####################################
# 목적 : title 텍스트를 전처리한다
# 기능 : 끝에붙은 대괄호와 안의 숫자, 콤마 (","), "u\202c" 를 제거한다
def preprocess_title(text):
    # 바꿀 것들 리스트
    replacements = {
        "\u202c": "",
        ',': ' '
    }
    for old, new in replacements.items():
        text = text.replace(old, new)       # replacements의 전자를 후자로 교체함
    result = re.sub(r'\[\d+\]$', '', text).strip()  # 뒤에 붙는 댓글수 [3]같은거 제거한다. + 공백제거
    if len(result) == 0:
        return "_"  # 널값이면 "_"을 리턴한다
    else:
        return result  # 전처리 결과값 리턴


#####################################
# get_url_row()
# 기능 : 검색결과에서 글 하나의 정보를 리턴한다
# 리턴값 : is_ignore(정보가 불필요하면 True, 필요하면 False), new_row(글 하나의 정보)
def get_url_row(element, search_info, blacklist, whitelist, start_date, end_date, max_retries=5):
    new_row = ["", "", "", 0, "", "", "", "", "", 0]
    is_ignore = False       # is_ignore이 True면, 이 함수를 사용하는 반복문을 탈출하도록 할 것입니다
    is_black = False        # 블랙리스트로 걸러졌는지 아닌지
    try:
        # [ignore 1. 너무 많이 재시도하면 스킵]
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_url_row()]")
            is_ignore = True
            return new_row, is_ignore, is_black    # 스킵
        # [ignore 2. 공지/광고글]
        author = element.find('td', class_='gall_writer').get_text().replace("\n", "").strip()    # 글쓴이
        if author == "운영자":            # 광고글은 글쓴이가 "운영자"
            is_ignore = True
            return new_row, is_ignore, is_black    # 광고글 스킵
        # [ignore 3. 블랙리스트]
        title = element.find('td', class_='gall_tit ub-word').find('a').get_text(strip=True)    # title
        if util.contains_any_from_list(title, whitelist):     # whitelist에 해당하는 단어 발견
            print("[WhiteList - 제목] : ", title)
            pass    # 제목에 whitellist의 단어가 있으면, 수집한다
        elif util.contains_any_from_list(title, blacklist):       # blacklist에 해당하는 단어 발견
            print("[BlackList - 제목] : ", title)
            is_ignore = True              # 제목에 blacklist의 단어가 있으면
            is_black = True
            return new_row, is_ignore, is_black     # 무시하고 넘어가기
        # [ignore 4. 날짜 조건]
        date_created = element.find('td', class_='gall_date')['title'][:10]               # 생성된 날짜
        date_created_datetime = datetime.strptime(date_created, "%Y-%m-%d")
        if end_date is not None:
            start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            if date_created_datetime > end_date_datetime:
                print("[시간 범위에 해당되지 않음 1]")
                is_ignore = True
                return new_row, is_ignore, is_black  # 스킵
            elif date_created_datetime < start_date_datetime:
                print("[시간 범위에 해당되지 않음 2]")
                is_ignore = True
                return new_row, is_ignore, is_black  # 스킵
        time_created = element.find('td', class_='gall_date')['title'][11:]               # 생성된 시각
        number = int(element.find('td', class_='gall_num').get_text())                    # 글 번호
        url = "https://gall.dcinside.com" + element.select_one("td.gall_tit a")['href']   # 글 url
        title = preprocess_title(title)                                                   # 글 제목
        recommend = element.find('td', class_='gall_recommend').get_text()                # 추천수
        new_row = [search_info["community"], search_info["gall_id"], search_info["search_keyword"], number, date_created, time_created, url, title, author, recommend]
    except Exception as e:
        print("[오류 발생, 반복] [get_url_row()] ", e)
        new_row, is_ignore, is_black = get_url_row(element, search_info, blacklist, whitelist, start_date, end_date, max_retries-1)
    return new_row, is_ignore, is_black


#####################################
# 기능 : 본문(post)에서 row 정보를 얻어온다
def get_post_row(url_row, soup, blacklist, whitelist, max_retries=3):
    is_ignore = False   # is_ignore이 True면, 이 함수를 사용하는 반복문을 탈출하도록 할 것입니다
    is_black = False    # 블랙리스트로 걸러졌는지 아닌지
    is_reply = 0        # 본문(post) 이므로 0
    new_row = ["", "", "", 0, "", "", "", is_reply, ""]
    try:
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_post_row()]")
            is_ignore = True
            is_black = False
            return new_row, is_ignore, is_black    # 스킵
        text = util.preprocess_text_dc(soup.find('div', {"class": "write_div"}).text)   # text를 불러오고, 전처리한다
        if util.contains_any_from_list(text, whitelist):  # text에 whitellist의 단어가 있으면, 수집한다
            print("[WhiteList - text] : ", text)
            pass
        elif util.contains_any_from_list(text, blacklist):  # text에 blacklist 단어가 있으면, 무시하고 넘어간다
            print("[BlackList - text] : ", text)
            is_ignore = True
            is_black = True
            return new_row, is_ignore, is_black
        text = url_row['title'] + " " + text    # title의 유의미한 정보를 text에 붙여준다
        # [크롤링한 정보를 new_row에 저장한다]
        new_row = [url_row['community'], url_row['gall_id'], url_row['search_keyword'], url_row['number'],
                   url_row['date_created'], url_row['time_created'], url_row['author'], is_reply, text]

    except Exception as e:
        print(f"[오류 : get_content_row()] ", e)
        new_row = get_post_row(url_row, soup, blacklist, whitelist, max_retries-1)
    return new_row, is_ignore, is_black


#####################################
# 기능 : 댓글 row를 만들어 리턴한다
# 리턴갑 : new_row
def get_reply_row(url_row, reply, start_date, end_date, max_retries=5):
    is_ignore = False
    is_reply = 1        # 댓글(reply) 이므로 0
    new_row = ["", "", "", 0, "", "", "", is_reply, ""]
    try:
        if max_retries <= 0:
            print("[최대 재시도 횟수 초과 : get_reply_row()]")
            is_ignore = True
            return new_row, is_ignore    # 스킵
        date_created, time_created = get_reply_date(reply)
        # [ignore : 날짜 조건]
        date_created_datetime = datetime.strptime(date_created, "%Y-%m-%d")
        if end_date is not None:
            start_date_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            if date_created_datetime > end_date_datetime:
                print("[시간 범위에 해당되지 않음 1]")
                is_ignore = True
                return new_row, is_ignore    # 스킵
            elif date_created_datetime < start_date_datetime:
                print("[시간 범위에 해당되지 않음 2]")
                is_ignore = True
                return new_row, is_ignore    # 스킵
        text = reply.find("p", {"class": "usertxt ub-word"}).text  # 댓글 내용 추출
        text = util.preprocess_text_dc(text)  # 전처리
        author = reply.select_one("span.nickname").get_text().strip()
        # [크롤링한 정보를 new_row에 저장한다]
        new_row = [url_row['community'], url_row['gall_id'], url_row['search_keyword'], url_row['number'],
                   date_created, time_created, author, is_reply, text]
    except Exception as e:
        print(f"[오류 : get_content_row()] ", e)
        new_row, is_ignore = get_reply_row(url_row, reply, start_date, end_date, max_retries-1)
    return new_row, is_ignore


#####################################
# 기능 : url을 받아 reply_list를 리턴합니다
# 리턴값 : reply_list
def get_reply_list(url, time_sleep=0, max_retries=100):
    try:
        if max_retries <= 0:
            return []
        driver = get_driver()
        driver.get(url)
        time.sleep(time_sleep)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        reply_list = soup.find_all("li", {"class": "ub-content"})
        driver.quit()
    except Exception as e:
        print(f"[오류 : get_reply_list(time_sleep={time_sleep})] ", e)
        reply_list = get_reply_list(url, time_sleep+1, max_retries-1)
    return reply_list


################################
# get_last_page()
# 기능 : [dcinside] 갤러리 내에서 검색결과의 마지막 페이지가 몇인지 리턴 (검색한 직후의 url이어야 함)
# 리턴값 : max_page(int)
def get_last_page(soup):
    paging_box = soup.find('div', class_='bottom_paging_wrap re')
    a_list = paging_box.select("div.bottom_paging_box a")
    len_a_list = len(a_list)
    for a in a_list:
        if a.find('span', class_='sp_pagingicon'):
            len_a_list -= 1
    last_page = len_a_list + 1
    if len(a_list) >= 17:    # page가 16개 이상이면 >> 버튼이 생기면서 a태그가 17개가 된다 / 이때의 페이징 처리
        last_page_url = a_list[-2]['href']   # 맨 마지막 페이지로 가는 버튼의 url
        last_page = re.search(r'page=(\d+)', last_page_url).group(1)     # 정규식으로 page 부분의 숫자만 추출
        return int(last_page)  # 맨 마지막 페이지
    else:
        return last_page  # 페이지 개수


##############################
# 기능 : 폴더 내 keyword와 일치하는 파일만 검색, 임시파일 어디까지 했는지 int 값으로 반환한다. 없으면 -1 반환
def get_done_index(keyword, folder_path_):
    max_number = -1
    pattern = re.compile(r"^(\d+)_temp_text_" + re.escape(keyword) + r".csv$")

    for filename in os.listdir(folder_path_):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            max_number = max(max_number, num)

    return max_number


##############################
# get_gall_id()
# 기능 : gall_url을 받아 gall_id를 리턴한다
def get_gall_id(gall_url):
    return re.search(r'id=([\w_]+)', gall_url).group(1)


#############################
# get_gall_type()
# 기능 : 메이저갤러리인지 마이너갤러리인지 미니갤러리인지 리턴한다
# 리턴값 : gall_type 문자열
def get_gall_type(gall_url):
    if "mgallery" in gall_url:  # 마이너갤러리
        gall_type = "minor"
    elif "mini" in gall_url:    # 미니갤러리
        gall_type = "mini"
    else:                       # 메이저갤러리
        gall_type = "major"
    return gall_type


##############################
# get_url_base()
# 기능 : 메이저갤러리인지 마이너갤러리인지 미니갤러리인지 판단한다
# 리턴값 : url_base
def get_url_base(gall_url):
    if "mgallery" in gall_url:  # 마이너갤러리
        url_base = "https://gall.dcinside.com/mgallery"
    elif "mini" in gall_url:    # 미니갤러리
        url_base = "https://gall.dcinside.com/mini"
    else:                       # 메이저갤러리
        url_base = "https://gall.dcinside.com"
    return url_base


#####################################
# 기능 : 댓글 html코드를 받아서, 댓글의 date를 리턴합니다
# 리턴값 : 2023-10-06 형식의 문자열
def get_reply_date(reply):
    temp_date = reply.find("span", {"class": "date_time"}).text.replace(".", "-")  # 댓글 등록 날짜 추출
    if temp_date[:2] == "20":  # 작년 이전은 "2022.09.07 10:10:54" 형식임
        date_created = temp_date[:10]
    else:  # 올해는 "09.30 10:10:54" 형식임
        date_created = str(datetime.now().year) + "-" + temp_date[:5]  # 올해 년도를 추가함
    time_created = temp_date[-8:]
    return date_created, time_created


#####################################
# is_ignore_reply()
# 기능 : 무시해야하는 댓글이면, True를 반환하고, 필요한 댓글이면 False를 반환합니다
def is_ignore_reply(reply):
    if reply.select_one("p.del_reply"):
        # print("[삭제된 코멘트입니다]")
        return True
    elif reply.find('span', {'data-nick': '댓글돌이'}):
        # print("[댓글돌이는 무시합니다]")
        return True
    elif reply.find('div', {'class': 'comment_dccon'}):
        # print("[디시콘은 무시합니다]")
        return True
    else:
        return False
