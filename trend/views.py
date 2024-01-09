from django.shortcuts import render
from .naverapi import get_news_data
from .naverapi import get_news_detail
from urllib.parse import quote, unquote
import random

def chat(request):
    # get_news_data 함수로 데이터 가져오기
    article_info = get_news_data("AI 챗봇")

    # 템플릿에 전달할 context 생성
    context = {
        'article_info': article_info,
        'title_text': "Chat Bot 기술",
    }

    return render(request, "trend/api_list.html", context)

def ocr(request):
    article_info = get_news_data("AI OCR")
    context = {
        'article_info': article_info,
        'title_text': "OCR 기술",
    }
    return render(request, "trend/api_list.html", context)

def trend(request):
    article_info = get_news_data("AI 대세")
    context = {
        'article_info': article_info,
        'title_text': "AI 기타정보",
    }
    return render(request, "trend/api_list.html", context)

def search(request, keyword):
    article_info = get_news_data(keyword)
    context = {
        'article_info': article_info,
        'title_text': '"' + keyword + '"의 검색결과',
    }
    return render(request, "trend/api_list.html", context)

def content(request, encoded_url):
    if encoded_url == "no_content":
        title = "없음"
        date = "없음"
        link = "없음"
        story = "없음"
    else:
        decoded_url = unquote(encoded_url)
        original_url = "https://n.news.naver.com/mnews/"+decoded_url
        article_detail = get_news_detail(original_url)
        title = article_detail['title']
        date = article_detail['date']
        link = article_detail['link']
        story = article_detail['story']

    random_img = 'trend/images/random_0'+str(random.randint(1, 8))+'.jpg'

    context = {
        'title': title,
        'date': date,
        'link': link,
        'story': story,
        'random_img': random_img,
    }
    return render(request, "trend/api_detail.html", context)