#############################################################################
# Kain7f1 / 2024-01-22
# config.py 파일에서 설정값을 입력합니다.


# 검색할 키워드(keyword)의 블랙리스트 : 목적에 맞지 않는 콘텐츠를 걸러내는 기능을 한다
blacklist = {
    "에코": ["http", "에코백", "에코페", "에코팰", "에코플", "에코마", "에코디", "에코랜", "에코스", "에코하", "아마존 에코"]  # 에코프로
    , "금양": ["http", "황금양", "금양말", "조금양", "지금양", "방금양", "금양전", "세금양"]
    , "기아": ["http", "기아니", "기아님", "기아닐", "기아닌", "기아이", "기아녀", "기아파트", "기아들", "급기아", "새기아", "사기아", "얘기아", "전기아", "광기아", "러기아", "자기아빠", "자기아들", "자기아는", "장기아프"]
    , "토스": ["http", "토스트", "도리토스", "치토스", "멘토스", "셀토스", "키보토스", "프로토스", "테스토스", "토스테론"]
    , "코스맥스": ["http", "맥도날드"]
    , "콜마": ["http", "콜마비"]
}

# 검색할 키워드(keyword)의 화이트리스트 : whitelist의 단어가 있으면, 유의미한 정보로 판단한다. 블랙리스트의 단어가 포함될지라도.
whitelist = {
    "기아": ["기아차", "기아자동차", "현대"]
}

# [갤러리 목록] "____" 갤러리
gall_url = {
    "실전주식투자": "https://gall.dcinside.com/mgallery/board/lists?id=jusik"
    , "코스피": "https://gall.dcinside.com/mgallery/board/lists?id=kospi"
    , "미국주식": "https://gall.dcinside.com/mgallery/board/lists?id=stockus"
    , "해외주식": "https://gall.dcinside.com/mgallery/board/lists/?id=tenbagger"
    , "주식": "https://gall.dcinside.com/board/lists/?id=neostock"
    , "재테크": "https://gall.dcinside.com/mgallery/board/lists?id=jaetae"
    , "부동산": "https://gall.dcinside.com/board/lists/?id=immovables"
    , "S&P500": "https://gall.dcinside.com/mini/board/lists/?id=snp500"
    , "다우": "https://gall.dcinside.com/mgallery/board/lists?id=dow100"
    , "나스닥": "https://gall.dcinside.com/mgallery/board/lists?id=nasdaq"
    , "증권": "https://gall.dcinside.com/mgallery/board/lists/?id=securities"
    , "금융": "https://gall.dcinside.com/mgallery/board/lists?id=finance"
    , "해외선물": "https://gall.dcinside.com/mgallery/board/lists?id=of"
    , "해외선물실전투자": "https://gall.dcinside.com/mini/board/lists/?id=kuya"
    , "국내선물옵션": "https://gall.dcinside.com/mini/board/lists/?id=koreafutures"
    , "캠퍼스개미": "https://gall.dcinside.com/mgallery/board/lists?id=smow"
    , "신용카드": "https://gall.dcinside.com/board/lists/?id=creditcard"
    , "체크카드": "https://gall.dcinside.com/mgallery/board/lists?id=checkcard"
    , "에너지주식": "https://gall.dcinside.com/mini/board/lists/?id=energystock"
    , "초전도체": "https://gall.dcinside.com/board/lists/?id=superconductor"
    , "편의점": "https://gall.dcinside.com/board/lists/?id=cs_new1"
    , "중세게임": "https://gall.dcinside.com/mgallery/board/lists?id=aoegame"
    , "검은사막": "https://gall.dcinside.com/board/lists/?id=bd"
    , "검은사막하이델": "https://gall.dcinside.com/mgallery/board/lists/?id=heidel"
    , "로스트아크": "https://gall.dcinside.com/board/lists/?id=lostark"
    , "중도정치": "https://gall.dcinside.com/mgallery/board/lists?id=centristpolitics"
    , "더불어민주당": "https://gall.dcinside.com/mgallery/board/lists?id=minjudang"
    , "이준석": "https://gall.dcinside.com/mgallery/board/lists?id=kids"
    , "안철수x국민의힘": "https://gall.dcinside.com/mgallery/board/lists?id=csahn"
    , "새로운보수당": "https://gall.dcinside.com/mgallery/board/lists?id=newconservativeparty"
    , "안철수": "https://gall.dcinside.com/board/lists/?id=ancheolsu"
    , "국민의힘": "https://gall.dcinside.com/mgallery/board/lists?id=alliescon"
    , "이재명": "https://gall.dcinside.com/mgallery/board/lists?id=leejaemyung"
}

#############################################################################################
#                                        << 설정값 >>
# [검색할 키워드를 설정합니다]
keyword = "펄어비스"
# [갤러리를 선택할 수 있습니다. 선택된 갤러리에서만 크롤링이 진행됩니다]
gall_name_list = [
    "검은사막하이델"
    # "코스피", "실전주식투자", "미국주식", "해외주식", "주식",
    # "재테크", "S&P500", "다우", "나스닥", "증권",
    # "금융", "해외선물", "해외선물실전투자", "국내선물옵션", "캠퍼스개미"
]

# [크롤링 기간을 설정할 수 있습니다]
# start_date = None
# end_date = None
start_date = "2023-12-01"
end_date = "2024-01-17"

# [blacklist, whitelist 의 디폴트 값을 설정할 수 있습니다]
try:
    blacklist_ = blacklist[keyword]     # blacklist 설정
except Exception:
    blacklist_ = ["http"]               # blacklist 디폴트 값
try:
    whitelist_ = whitelist[keyword]     # whitelist 설정
except Exception:
    whitelist_ = None                   # whitelist 디폴트 값

###############################################################################################################
#                                            << 실행하는 곳 >>
# for gall_name in gall_name_list:
#     crawl_url(gall_url[gall_name], keyword, blacklist_, whitelist_, start_date, end_date)  # [1. url 크롤링]
for gall_name in gall_name_list:
    crawl_text(gall_url[gall_name], keyword, blacklist_, whitelist_, start_date, end_date)  # [2. text 크롤링]

# util.merge_crawling_results(keyword)    # [옵션 : 크롤링 전부 끝나면, 결과와 로그 파일을 합쳐서 저장한다]

#########################################################

# [옵션 : 2개 이상 키워드로 검색한 경우, url 크롤링 결과를 합친다]
# util.merge_url_crawling_results(keyword, gall_name_list)


