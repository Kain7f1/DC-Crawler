#############################################################################
# 만든이 : Kain7f1
# 생성일 : 2023-10-08
# 전제 : 실행하기 전에, Users 폴더에 chromedriver.exe를 현재 크롬 버전에 맞게 다운받아주세요
# 기능 : dcinside 크롤링 실행 함수

from dcinside_crawler import crawl_url, crawl_text
import utility_module as util
#############################################################################
#                                 << 설정값 >>
keyword = "에코"       # 검색할 키워드
gall_name = "캠퍼스개미"    # 검색할 갤러리 선택하기


# 검색할 키워드(keyword)의 블랙리스트 : 목적에 맞지 않는 콘텐츠를 걸러내는 기능을 한다
blacklist = {
    "에코프로": ["http"]
    , "에코": ["http", "에코백", "에코페", "에코팰", "에코플", "에코마", "에코디", "에코랜", "에코스", "에코하", "아마존 에코"] # 에코프로
    , "금양": ["http", "황금양", "금양말", "조금양", "지금양", "방금양", "금양전", "세금양"]
    , "피엔티": ["http"]
    , "엘앤에프": ["http", "하반기"]
    , "lg화학": ["http"]
    , "두산퓨얼셀": ["http"]  # 두산퓨얼셀

    , "에스엠": ["http"]
    , "하이브": ["http"]
    , "카카오": ["http"]

    , "코스맥스": ["http"]
    , "아모레": ["http"]
    , "콜마": ["http"]  # 한국콜마
    , "휴젤": ["http"]

    , "현대차": ["http"]   # 제안 : 현대자동차도 검색?
    , "기아": ["http", "기아니", "기아님", "기아닐", "기아닌", "기아이", "기아녀", "기아파트", "기아들", "급기아", "새기아", "사기아", "얘기아", "전기아", "광기아", "러기아", "자기아빠", "자기아들", "자기아는", "장기아프"]

    , "토스": ["http", "토스트", "도리토스", "치토스", "멘토스", "셀토스", "키보토스", "프로토스", "테스토스", "토스테론"]
}

# 검색할 키워드(keyword)의 화이트리스트 : whitelist의 단어가 있으면, 유의미한 정보로 판단한다. 블랙리스트의 단어가 포함될지라도.
whitelist = {
    "엘앤에프": ["플레이"]
    , "기아": ["기아차", "기아자동차", "현대"]
}

# [갤러리 목록] "____" 갤러리
gall_url = {
    "실전주식투자": "https://gall.dcinside.com/mgallery/board/lists?id=jusik"
    , "코스피": "https://gall.dcinside.com/mgallery/board/lists?id=kospi"
    , "미국주식": "https://gall.dcinside.com/mgallery/board/lists?id=stockus"
    , "해외주식": "https://gall.dcinside.com/mgallery/board/lists/?id=tenbagger"
    , "재테크": "https://gall.dcinside.com/mgallery/board/lists?id=jaetae"
    , "부동산": "https://gall.dcinside.com/board/lists/?id=immovables"         # 부동산갤 blacklist : ["서울말", "경출요뽑요", "조희팔"]
    , "슨피": "https://gall.dcinside.com/mini/board/lists/?id=snp500"
    , "다우": "https://gall.dcinside.com/mgallery/board/lists?id=dow100"
    , "나스닥": "https://gall.dcinside.com/mgallery/board/lists?id=nasdaq"
    , "증권": "https://gall.dcinside.com/mgallery/board/lists/?id=securities"
    , "금융": "https://gall.dcinside.com/mgallery/board/lists?id=finance"
    , "해외선물": "https://gall.dcinside.com/mgallery/board/lists?id=of"
    , "해외선물실투": "https://gall.dcinside.com/mini/board/lists/?id=kuya"
    , "국내선물옵션": "https://gall.dcinside.com/mini/board/lists/?id=koreafutures"
    , "캠퍼스개미": "https://gall.dcinside.com/mgallery/board/lists?id=smow"
    , "신용카드": "https://gall.dcinside.com/board/lists/?id=creditcard"
    , "체크카드": "https://gall.dcinside.com/mgallery/board/lists?id=checkcard"
    , "에너지주식": "https://gall.dcinside.com/mini/board/lists/?id=energystock"
    , "초전도체": "https://gall.dcinside.com/board/lists/?id=superconductor"
    , "편의점": "https://gall.dcinside.com/board/lists/?id=cs_new1"
}

###############################################################################################################
#                                            << 실행하는 곳 >>
# [whitelist 존재하지 않을 때]
# crawl_url(gall_url[gall_name], keyword, blacklist[keyword])                        # [1. url 크롤링]
crawl_text(gall_url[gall_name], keyword, blacklist[keyword])                       # [2. text 크롤링]

# [whitelist 있을 때]
# crawl_url(gall_url[gall_name], keyword, blacklist[keyword], whitelist[keyword])    # [1. url 크롤링]
# crawl_text(gall_url[gall_name], keyword, blacklist[keyword], whitelist[keyword])   # [2. text 크롤링]

# [옵션 : 키워드 여러개로 검색하고, 파일 합치기]
# util.merge_csv_files(save_file_name=f"merged_{keyword}", read_folder_path_="./url/crawling_result", save_folder_path_="./url/merged_files", subset='number')

###############################################################################################################
