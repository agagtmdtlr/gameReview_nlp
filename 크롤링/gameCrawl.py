import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import selenium.common.exceptions

url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=ko&showAllReviews=true'
# driver 경로는 본인 chromedriver.exe 파일이 존재하는 경로로 설정
filepath = 'd:/chromedriver.exe'

driver = webdriver.Chrome(filepath)
# selenium은 request 객체로 get하지 않는다.
# request = urllib.request.Request(url)
driver.get(url)
driver.implicitly_wait(3)

body = driver.find_element_by_css_selector('body')

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    try:
        element = body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ')
        if element is not None:
            element.click()
            break
    except Exception as err:
        print(err)
        continue
count = 0
begin = 0
more = 1
while count-begin <= 40: # 스크롤 40번 까지 실행해도 더보기 버튼이 없으면 끝인걸로 판별하여 작업 중단
    count +=1
    # print(count)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1) # 데이터 로딩 시간 대기
    try:
        #button

        element = body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d')
        if element is not None:
            element.click()
            print(count)
            begin = count # 마지막 더보기 버튼 눌렀을때의 카운트 저장
            time.sleep(more)
            # 지연 시간 보정
            more += 0.1
    # 더보 기 버튼 없을 경우 : 스크롤 반복
    except selenium.common.exceptions.NoSuchElementException as err:
        print(err)
        try:
            continue
        except Exception as err:
            print(err)
            break
    except Exception as err:
        print(err)
        break

    # 더 보기 class name
    #U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d
    #U26fgb O0WRkf oG5Srb C0oVfc n9lfJ M9Bg4d

# 리뷰 상세 더 보기 전부 다 클릭
try:
    body = driver.find_element_by_css_selector('body')
    lists = body.find_elements_by_css_selector('.LkLjZd.ScJHi.OzU4dc')
    if lists is not None:
        for btn in lists:
            btn.click()
            time.sleep(0.2)
except:
    pass
page = driver.page_source
with open(file='../concat_data/brawlstarz_review.txt', mode='w', encoding='utf-8') as file :
    file.write(page)
soup = BeautifulSoup(page,'html.parser')

lists = soup.select('bN97Pc')

