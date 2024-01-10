from django.shortcuts import render
import requests
import json
from bs4 import BeautifulSoup
import random

def ai_pg(request):
    return render(request, "ai_pg/ai_pg.html")

def ai_tool_guide(request):
    return render(request, 'ai_pg/ai_tool_guide.html')

def ai_sld(request):
    # parent_id = '5616a311dfa346e59458ba8ecb7baaed'
    # workspace_data = get_workspace_data(parent_id)
    # print(workspace_data)

    access_id = '5616a311dfa346e59458ba8ecb7baaed'
    context={}
    notion_page_data = get_notion_page_content(access_id)
    context['page_content'] = notion_page_data
    file_path = "C:\\KDT\\workspace\\m4_웹개발\\django_project\\ai_pg\\workspace_data.json"
    with open(file_path, 'r', encoding='utf-8') as json_file:
        workspace_data = json.load(json_file)
    context['workspace_data'] = workspace_data
    context['notion_page_title'] = "파이썬"
    return render(request, 'ai_pg/ai_sld.html', context)

def ai_sld_detail(request, notion_page_id):
    access_id = '5616a311dfa346e59458ba8ecb7baaed'
    context={}
    if notion_page_id:
        context['is_second'] = "yes"
        access_id = notion_page_id.replace("-","")
    notion_page_data = get_notion_page_content(access_id)
    context['page_content'] = notion_page_data
    file_path = "C:\\KDT\\workspace\\m4_웹개발\\django_project\\ai_pg\\workspace_data.json"
    with open(file_path, 'r', encoding='utf-8') as json_file:
        workspace_data = json.load(json_file)
    context['workspace_data'] = workspace_data
    context['notion_page_title'] = find_title_by_id(workspace_data, notion_page_id)
    return render(request, 'ai_pg/ai_sld.html', context)

def ai_pjrv(request):
    kaggle_info = []
    # url = "https://www.kaggle.com/code"
    # response = requests.get(url)

    file_path = "C:\\KDT\\workspace\\m4_웹개발\\django_project\\ai_pg\\kaggle_soup.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        kaggle_soup = file.read()
    soup = BeautifulSoup(kaggle_soup, 'html.parser')

    for kaggle_item in soup.find_all('div', class_=['sc-ggTfmB', 'sc-dfzfrJ', 'gtcKUi', 'jkIfEH']):
        check1 = kaggle_item.select_one('a img.sc-jnyqrv.jyThNi')
        thumbnail_url = check1['src'] if check1 and 'src' in check1.attrs else ''
        thumbnail_url = set_alternative_image(thumbnail_url)

        check2 = kaggle_item.select_one('.sc-irTswW.sc-gtoQIa')
        title = check2.get_text(strip=True) if check2 else ''

        check3 = kaggle_item.select_one('.sc-fGFwAa.sc-bPoMgM')
        vote_count = check3.get_text(strip=True) if check3 else ''

        check4 = kaggle_item.select_one('span.sc-fmSAUk.sc-ysCxF span')
        show_date = check4['title'][:16] if check4 else ''

        check5 = kaggle_item.select_one('a.sc-kMDPuR.enKBuM')
        url_short = check5['href'] if check5 and 'href' in check5.attrs else ''
        url = "https://www.kaggle.com" + url_short

        kaggle_info.append({'thumbnail_url': thumbnail_url, 'title': title, 'vote_count': vote_count, 'show_date': show_date, 'url': url })
    
    return render(request, 'ai_pg/ai_pjrv.html', {'kaggle_info': kaggle_info})


#### 노션
# 노션 API를 통해 페이지의 내용을 가져오는 함수
def get_notion_page_content(access_id):
    url = f'https://api.notion.com/v1/blocks/{access_id}/children'
    notion_token = 'secret_5GOiKCVt6kcK5U00K8NVXecECbPErMsm7ildsMSQRiz' 
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    response = requests.get(url, headers=headers)
    notion_data = response.json()
    # 필요한 데이터 추출 및 가공 로직
    processed_data = []
    for block in notion_data.get('results', []):
        if block.get('type') == 'heading_2':
            content = block.get('heading_2', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
        elif block.get('type') == 'heading_3' or block.get('type') == 'bulleted_list_item' or block.get('type') == 'code':
            # 코드 블록의 경우 'code' 필드에 내용이 있습니다.
            content = block.get('code', {}).get('rich_text', [{}])[0].get('text', {}).get('content', '')
        else:
            # 위의 경우에 해당하지 않는 블록 타입인 경우에도 content를 설정
            content = block.get('rich_text', [{}])[0].get('text', {}).get('content', '')
        
        # 해당 내용을 'content' 필드에 추가
        block['content'] = content
        
        processed_data.append(block)
    return processed_data

def get_workspace_data(page_id):
    notion_token = 'secret_5GOiKCVt6kcK5U00K8NVXecECbPErMsm7ildsMSQRiz'
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'

    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return process_notion_data(data)
    else:
        # Handle the error, for example, print the error message
        print(f"Failed to retrieve child pages. Status code: {response.status_code}")
        print(response.json())
        return []

def process_notion_data(notion_data):
    processed_data = []
    for block in notion_data.get('results', []):
        if block.get('type') == 'child_page':
            title = block.get('child_page', {}).get('title', '')
            child_id = block.get('id')
            children = get_workspace_data(child_id)  # Recursively fetch children
            processed_data.append({'id': child_id, 'title': title, 'children': children})
    return processed_data

def find_title_by_id(data, target_id):
    for node in data:
        if node['id'] == target_id:
            return node['title']
        if 'children' in node and node['children']:
            result = find_title_by_id(node['children'], target_id)
            if result:
                return result
    return None

def set_alternative_image(image_url):
    # "/static/images/kernel/" 또는 "/kf/156455559/eyJhbGciOiJka"이 포함되어 있으면 대체 URL로 변경
    if "/static/images/kernel/" in image_url:
        random_seed = random.randint(1, 100)
        alternative_url = f'https://picsum.photos/seed/{random_seed}/400/300'
        return alternative_url
    else:
        return image_url