import requests
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup

def get_thumbnail(url):
    # 웹 페이지에서 HTML을 가져오기
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 썸네일 이미지 URL을 찾기
    thumbnail_tag = soup.find('meta', {'property': 'og:image'})
    if thumbnail_tag:
        thumbnail_url = thumbnail_tag['content']
        return thumbnail_url
    else:
        print("썸네일을 찾을 수 없습니다.")
        return None

def get_news_data(category):
    client_id = "3G4KCuMKuOl3PUjDuP8i"  # api Client ID
    client_secret = "zGyTrIEtyo"  # api Client Secret
    search_word = category  # 검색어
    encode_type = 'json'  # 출력 방식 json 또는 xml
    sort = 'sim'  # 결과값의 정렬기준 시간순 date, 관련도 순 sim

    max_display = 32  # 수집 뉴스 수
    start = 1  # 출력 위치

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
               'X-Naver-Client-Secret': client_secret
               }

    # HTTP 요청
    r = requests.get(url, headers=headers)

    articles = []

    if r.status_code == 200:
        # 현재 날짜 구하기
        today = datetime.now().strftime('%Y%m%d')

        for index, data in enumerate(r.json()['items']):
            pub_date_str = data['pubDate']
            pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')

            # 30일 전 날짜 계산
            thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

            # pubDate가 30일 이내인 경우에만 처리
            if pub_date.strftime('%Y%m%d') >= thirty_days_ago:
                title = re.sub('(<([^>]+)>)', '', data['title'])
                title = re.sub('&quot;', '"', title)
                title = title.replace('…', '.').replace('..', '.').replace('…', '.')
                contents = re.sub('(<([^>]+)>)', '', data['description'])
                contents = re.sub('&quot;', '"', contents)
                contents = contents.replace('…', '.').replace('..', '.').replace('…', '.')
                url = data['link']
                url_prm = url[31:]

                # 추가: url이 'news.naver.com'을 포함하는 경우에만 처리
                if 'news.naver.com' in url:
                    # show_date 생성
                    show_date = pub_date.strftime('%Y년 %m월 %d일 %A')

                    # 수정: get_thumbnail 함수를 이용하여 썸네일 URL 가져오기
                    thumbnail_url = get_thumbnail(url)

                    articles.append({
                        'title': title,
                        'contents': contents,
                        'url': url,
                        'url_prm': url_prm,
                        'reg_date': pub_date_str,  # pubDate 그대로 저장
                        'show_date': show_date,    # 수정: show_date 저장
                        'thumbnail_url': thumbnail_url
                    })
                
            # 추가: articles 리스트의 길이가 10이 되면 루프 종료
            if len(articles) == 10:
                break

    else:
        print('검색 실패')

    return articles

def story_process(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # data-src를 src로 치환
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        if 'data-src' in img_tag.attrs:
            img_tag['src'] = img_tag['data-src']
            del img_tag['data-src']
    
    # 쉼표 제거
    for tag in soup.find_all():
        if tag.name == 'script':
            continue  # script 태그는 건너뜀
        if tag.string:
            tag.string = tag.string.replace(',', '')
    
    return str(soup)

def get_news_detail(original_url):
    # 웹페이지의 HTML 가져오기
    url = original_url
    response = requests.get(url)
    html_content = response.text

    # BeautifulSoup으로 HTML 컨텐츠 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 값 추출 실행. get_text 에러 발생시 None값 치환
    title_element = soup.find('h2', {'id': 'title_area', 'class': 'media_end_head_headline'})
    title = title_element.get_text(strip=True) if title_element else None

    date_element = soup.find('span', {'class': 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME'})
    date = date_element.get_text(strip=True) if date_element else None

    story_element = soup.find('article', {'id': 'dic_area', 'class': 'go_trans _article_content'})
    story_html = story_process(str(story_element))

    art_detail = {
        'title': title,
        'date': date,
        'link': url,
        'story': story_html
    }

    return art_detail
