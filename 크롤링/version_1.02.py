import time
import selenium.common.exceptions

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


### 경로 ###
url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=ko&showAllReviews=true'
filepath = 'd:/chromedriver.exe'

### 드라이버 구동 ####
driver = webdriver.Chrome(filepath)
driver.get(url)
driver.implicitly_wait(3)

### selenium 무한 스크롤링 ########
body = driver.find_element_by_css_selector('body')
last_height = driver.execute_script("return document.body.scrollHeight")
#### 첫번째 더보기 버튼 까지 #####
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(3)
    try:
        element = body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ')
        if element is not None:
            element.click()
            driver.implicitly_wait(3)
            break
    except Exception as err:
        print(err)
        continue

#####################  method defined ########################################
def cycleScroll(times):
    scroll_wait = times
    try:
        # 더보기 버튼 클릭 작업
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        element = body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d')
        if element is not None:
            # 버튼이 있으면 클릭하기
            element.send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
    except selenium.common.exceptions.NoSuchElementException as err:
        # 더보기 버튼이 없을 시 스크롤 작업
        print(err)
    except Exception as err:
        print(err)

def checkHeight(point = 0):
    end = False # 계속 진행해도 됨 : False / 멈춰야됨 : True
    global last_height
    print(point)
    try:
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(new_height,',',last_height)
        if new_height == last_height :
            if point == 0:
                # 먹통일 경우 기회를 한번 줘서 올렸다 내리게 하기
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
                time.sleep(10)
                cycleScroll(10)
                end = checkHeight(point+1)
            else :
                end = True
            return end
        else:
            # 계속 해도됨
            last_height = new_height
            end = False
            return end
    except Exception as err:
        print(err,'\ncheckHeight')
        end = True
        return end
#####################  method defined ########################################

#### 첫번째 더보기 버튼 이후 끝까지
while True:
    cycleScroll(2)
    end = checkHeight()
    # print(end)
    if end :
        break
    # 더 보기 class name



##### page source 가져워 파일에 저장 test,csv#####
page = driver.page_source
##### raw concat_data to text ###
with open(file='../concat_data/brawlstarz_review_text_05.txt', mode='w', encoding='utf-8') as file :
    file.write(page)
######## parsing concat_data to csv #####
soup = BeautifulSoup(page,'html.parser')
lists = soup.select('div[jsmodel=y8Aajc]')
import csv
with open(file='concat_data/brawlstarz_review_soup_05.csv', mode='w', encoding='utf-8') as file :
    wr = csv.writer(file)
    for item in lists:
        score = item.select_one('div[class=pf5lIe]').select_one('div')['aria-label']
        day = item.select_one('span[class=p2TkOb]').text
        text = item.select_one('span[jsname=bN97Pc]').text
        text2 = item.select_one('span[jsname=fbQN7e]').text

        if len(text2) == 0:
            final = text
        else:
            final = text2
        wr.writerow([score,day,final])
driver.quit()