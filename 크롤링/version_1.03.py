import time
import selenium.common.exceptions
from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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



startpoint = 3

def deleteElement(s):
    print('deleteElement')
    global startpoint
    reverse = startpoint
    for i in count(startpoint):
        try:
            reverse += 1
            #yf3HXc;_;$3 YjFXEf;_;$2
            #yf3HXc;_;$43 YjFXEf;_;$44
            element = driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;${} YjFXEf;_;${}"]'.format(i,s))
            driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, element)
            driver.implicitly_wait(2)
        except selenium.common.exceptions.NoSuchElementException as err:
            print(err)
            startpoint = reverse
            break


deleteElement(2)
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


check = 203
cnt = 0
end = False
#####################  method defined ########################################
def cycleScroll(times):
    scroll_wait = times
    global check
    check += 40
    try:
        # 더보기 버튼 클릭 작업
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # jsdata = yf3HXc;_;$203 YjFXEf;_;$44
        # jscontroller="H6eOGe" jsmodel="y8Aajc"
        element = body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsdata='yf3HXc;_;${} YjFXEf;_;$44']".format(check))))

        if element is not None:
            # 버튼이 있으면 클릭하기
            element.send_keys(Keys.ENTER)
            driver.implicitly_wait(10)
        return False
    except selenium.common.exceptions.NoSuchElementException as err:
        # 더보기 버튼이 없을 시 스크롤 작업
        print(err)
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[jsdata='yf3HXc;_;${} YjFXEf;_;$44']".format(check))))
            return False
        except Exception as err:
            print('no find element',err)
            return True

    except Exception as err:
        print(err)
        return True

def checkHeight(point = 0):
    global end
    global last_height
    end = False  # 계속 진행해도 됨 : False / 멈춰야됨 : True
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
                return end
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



def savefile(filenum):
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    lists = soup.select('div[jsmodel=y8Aajc]')
    import csv
    with open(file='concat_data/brawlstarz_review_soup_{}.csv'.format(filenum), mode='w', encoding='utf-8') as file:
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
            wr.writerow([score, day, final])

#####################  method defined ########################################

#### 첫번째 더보기 버튼 이후 끝까지
filenum = 1
startelement = 3
element = 0
while True:
    ends = cycleScroll(2)
    if ends :
        break
    ends = checkHeight()
    # print(end)
    if ends :
        break
    cnt += 1
    if cnt == 3:
        savefile(filenum)
        deleteElement(44)
        filenum +=1
        cnt = 0
    print(cnt)
    # 더 보기 class name



# ##### page source 가져워 파일에 저장 test,csv#####
# page = driver.page_source
# ##### raw concat_data to text ###
# with open(file='concat_data/brawlstarz_review_text_06.txt', mode='w', encoding='utf-8') as file :
#     file.write(page)
# ######## parsing concat_data to csv #####
# soup = BeautifulSoup(page,'html.parser')
# lists = soup.select('div[jsmodel=y8Aajc]')
# import csv
# with open(file='concat_data/brawlstarz_review_soup_06.csv', mode='w', encoding='utf-8') as file :
#     wr = csv.writer(file)
#     for item in lists:
#         score = item.select_one('div[class=pf5lIe]').select_one('div')['aria-label']
#         day = item.select_one('span[class=p2TkOb]').text
#         text = item.select_one('span[jsname=bN97Pc]').text
#         text2 = item.select_one('span[jsname=fbQN7e]').text
#
#         if len(text2) == 0:
#             final = text
#         else:
#             final = text2
#         wr.writerow([score,day,final])
driver.quit()