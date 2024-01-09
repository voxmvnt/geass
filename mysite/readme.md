#### django_class 폴더 생성

#### 가상환경 생성
-윈도 : python -m venv myenv
-리눅스 : python3 -m venv myenv

#### 가상환경 활성화
-윈도 : myenv\Scripts\activate
-리눅스 : source myenv/bin/activate
-Ctrl+shift+p: select 인터프리터 > 가상환경 선택(myenv)

#### 가상환경 종료
-deactivate

#### requirements 설치
pip install -r requirements.txt

#### 새 프로젝트 (mysite라는 프로젝트 폴더 생성)
django-admin startproject mysite .

#### DB 생성
python manage.py migrate
>> db.sqlite3 생성됨.

#### 관리자 계정
python manage.py createsuperuser
아이디/비번: admin/admin 

#### 서버 실행 (서버 중단. 터미널에서 Ctrl+C)
python manage.py runserver

#### admin 접속 (장고 제공 관리자 페이지)
http://127.0.0.1:8000/admin/
여기서 아이디, 비밀번호 써서 접속

#### 앱 만들기
python manage.py startapp blog
python manage.py startapp single_pages

#### 앱 등록 (settings.py)
INSTALLED_APPS 부분에 앱이름 추가 

#### 주소 추가 (urls.py)
- 선행작업: from django.urls import path, include  (include 추가)
- 하단 path 추가. (아무것도 없을 경우 싱글페이지의 urls를 참고한다.)
path('', include("single_pages.urls")),
- single_pages의 urls파일에서도 반복작업 (파일 참고)
- 장고에서 templates 폴더는 html파일이 있는 곳으로 인식함

#### 구글 개발자 콘솔
- 새 프로젝트와 클라이언트 만들기 - console.developers.google.com 에 접속
- 새 프로젝트 생성 > 만들기 > OAuth 동의화면 "외부" 선택 > 앱이름
- 사용자 인증 정보 > 사용자 인증 정보 만들기 > OAuth 클라이언트 ID > 만들기 (유형, 이름, URL, URI 입력)
  >> 유형: 웹 애플리케이션  / 이름: geass 
  >> 승인된 자바스크립트 원본 : http://127.0.0.1:8000
  >> 승인된 리디렉션 URI : http://127.0.0.1:8000/accounts/google/login/callback/
- 생성된 id 및 비밀번호 저장 후 제이슨 파일도 다운로드
  >> id: 383414319132-hvcl3p7kj404rtrqf0iuv0i2du4geqe1.apps.googleusercontent.com
  >> pw: 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
  >> 제이슨 파일 mysite 폴더 내 있음

#### 데이터 백업 및 가져오기
python manage.py dumpdata > data_backup.json
python manage.py flush
python manage.py loaddata data_dump.json