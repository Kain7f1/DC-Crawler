# DC-Crawler

* DC-Crawler
  * 개요
  * 설정값
  * How to Use
  * Contacts
  * License

---

## 개요
대한민국 커뮤니티 dcinside의 게시글, 게시글에 달린 댓글을 크롤링합니다

## Requirements
[requirements.txt](https://github.com/Kain7f1/DC-Crawler/blob/main/requirements.txt) 에 기재되어 있습니다
* pandas==2.1.1
* numpy==1.26.0
* beautifulsoup4==4.12.2
* selenium==3.14.0
* requests==2.31.0

## 설정값
모든 설정은 main 함수에서 이루어집니다

### blacklist
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/efdf20f4-a25e-4b6f-9777-0dd8d7f27376)
* 목적에 맞지 않는 콘텐츠를 걸러내는 기능을 합니다
* ex) `기아`라는 기업에 대해 검색하는데, `사기아님`, `거기아닐까`, `여기아니야` 같은 불필요한 키워드가 포함된 글을 걸러낼 수 있습니다

### whitelist
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/d1a82c24-84fb-47b1-81fe-3c0a5a98942c)
* blacklist로 걸러진 글이더라도, whitelist의 단어가 포함되면 유의미한 데이터로 간주하고 수집합니다
* ex) `기아차 완전 사기아님?` 이라는 글이 blacklist로 걸러지는 것을 방지합니다

### gall_url
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/eb0cf36e-074e-4014-b250-68f346a2f1ae)
* 갤러리 이름과 url을 설정합니다

### keyword
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/8a7b4bcd-9f6b-40a9-932d-0d1d23865125)
* 검색할 키워드를 설정합니다

### gall_name_list
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/a9ca285c-bbc8-4ce7-b135-54fa557514a0)
* 갤러리를 선택할 수 있습니다. 선택된 갤러리에서만 크롤링이 진행됩니다

### start_date, end_date
![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/10ed836c-1be0-4e16-8e9e-67608d9e49c7)
* 크롤링 기간을 설정할 수 있습니다.
* 기간에 관계 없이 존재하는 모든 데이터를 크롤링하려면 None으로 설정합니다

---

## How to Use

![image](https://github.com/Kain7f1/DC-Crawler/assets/141689851/57428171-69e3-4ba0-94c1-4db2c1b97e5e)

설정값을 입력한 후, 한번에 실행하면 됩니다

* crawl_url() : 게시글 url 수집
* crawl_text() : 게시글/댓글 text 수집
* merge_crawling_results() : 수집 결과를 하나로 합친다


## Contacts

### 이슈 관련
* https://github.com/Kain7f1/DC-Crawler/issues

### E-mail
* kain7f1@gmail.com

## License

`DC-Crawler`는 `GPL-3.0 license` 라이선스 하에 공개되어 있습니다. 모델 및 코드를 사용할 경우 라이선스 내용을 준수해주세요. 라이선스 전문은 `LICENSE` 파일에서 확인하실 수 있습니다.
