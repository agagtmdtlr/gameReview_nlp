from pdb import main
import pandas as pd
import csv
import re
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
class Crawl:


    def __init__(self):
        # 브롤스타즈 전체리뷰 보기 페이지 path
        '''
        비동기 데이터 처리 방식의 페이지 이기 때문에 페이지 이동은 없으므로
        고정된 하나의 페이지에서 모든 작업을 수행한다.
        '''
        crawl_page_url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=ko&showAllReviews=true'

        # selenium control driver.exe path
        # please download matched your computer download browser version
        driver_path = 'C:/Users/brian/Desktop/dev_exe/chromedriver.exe'

        # 드라이버 구동
        # 모든 작업은 이 드라이버 인스턴스 하나로 끝낸다!!!!
        self.driver = webdriver.Chrome(driver_path)
        # move page
        self.driver.get(crawl_page_url)
        self.driver.implicitly_wait(3)

        ### selenium 무한 스크롤링 ########
        self.body = self.driver.find_element_by_css_selector('body')
        scrollheight = self.driver.execute_script("return document.body.scrollHeight")
        print(scrollheight)





    def setting_crawl_loop(self):
        '''
        scroll( window.scrollTo ) and automatically make element (implicitly_wait)
        by javascript
        and keep scroll and stop when find button element

        if you find button??
        conglatulation you finish crawl setting

        :return:
        boolean if work success return True other False
        '''
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(3)
            try:
                element = self.body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ')
                # 버튼을 찾으면 세팅이 끝났습니다.
                if element:
                    print("축하합니다 본격전인 크롤링을 위한 세팅이 끝났습니다.\n"
                          "즐거운 작업하시고 행복한 하루 되세요^^")
                    return True
            except seleExcep.NoSuchElementException as err:
                print("no button's element so keep working",err)
                continue
            except Exception as err:
                print("unexpected error",err)
                return False


    def crawl_review(self):
        try:
            element = self.body.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ')
            if element:
                element.send_keys(Keys.ENTER)
                self.driver.implicitly_wait(10)
        except:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.driver.implicitly_wait(3)
    def save_to_file(self):
        # 최종 파일은 directory : concat_data/brawlstarz_review_soup
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        lists = soup.select('div[jsmodel=y8Aajc]')
        try:
            with open(file='./../concat_data/brawlstarz_review_google2.csv', mode='w', encoding='utf-8') as file:
                wr = csv.writer(file)
                for item in lists:

                    score = item.select_one('div[class=pf5lIe]').select_one('div')['aria-label'][10]

                    date = item.select_one('span[class=p2TkOb]').text
                    # 년, 월, 일 속정 구분해서 저장
                    year,month,day = re.findall('[0-9]{1,}',date)

                    # 둘중에 하나만 들어가진다
                    text = item.select_one('span[jsname=bN97Pc]').text
                    text2 = item.select_one('span[jsname=fbQN7e]').text

                    # 리뷰내용 전체보기 내용이 없을경우 1번 element
                    # 있을 경우 2번 element를 리뷰 텍스트로 사용
                    if len(text2) == 0:
                        final = text
                    else:
                        final = text2
                    wr.writerow([score, year, month, day, final])
        except FileNotFoundError as err:
            print(err)
        except Exception as err:
            print(err)

    def quit_driver(self):
        self.driver.quit()

if __name__ == '__main__':
    crawl = Crawl()
    check = crawl.setting_crawl_loop()
    # print(check)
    try:
        for x in range(3000):
            crawl.crawl_review()
    except:
        pass
    crawl.save_to_file()
    crawl.quit_driver()

    # 저장한 파일 크기 확인하기
    # df = pd.read_csv('./../concat_data/brawlstarz_review_google.csv')
    # print(len(df))
