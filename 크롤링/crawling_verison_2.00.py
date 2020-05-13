import selenium
import selenium.common.exceptions as seleExcep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from itertools import count
from bs4 import BeautifulSoup

'''
크롤링 작업 순서도
0. 드라이버 작동 시작
1. 페이지로 이동
2. 스크롤 or 더보기 버튼 클릭으로 ajax 요청처리 (selenium 동적 처리)
3. 비동기 처리 추가 필요 여부 판단 ( 서버로 부터 요청할 데이터가 더 있는지 확인 ) 
4. [2]작업 중지 
5. 생성한 page source 저장
6. beautifulSoup을 통해 parse tree 생성하기
7. 필요한 데이터 추출
8. 추출 데이터 파일 저장
'''

# 브롤스타즈 전체리뷰 보기 페이지 path
'''
비동기 데이터 처리 방식의 페이지 이기 때문에 페이지 이동은 없으므로
고정된 하나의 페이지에서 모든 작업을 수행한다.
'''
crawl_page_url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=ko&showAllReviews=true'

# selenium control driver.exe path
# please download matched your computer download browser version
driver_path = 'd:/chromedriver.exe'

# 드라이버 구동
driver = webdriver.Chrome(driver_path)
driver.get(crawl_page_url)
driver.implicitly_wait(3)