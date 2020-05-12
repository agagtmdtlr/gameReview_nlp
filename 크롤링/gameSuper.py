import time
import csv
import selenium.common.exceptions
from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Crawl:
    url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&hl=ko&showAllReviews=true'
    filepath = 'd:/chromedriver.exe'
    filenum = 1
    check = 84
    delck = 84
    def __init__(self):
        self.driver = webdriver.Chrome(self.filepath)
        self.driver.get(self.url)
        self.driver.implicitly_wait(3)
        self.firstProcess()
        #83까지
        self.last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.point = 0

    def checkHeight(self):
        self.end = False  # 계속 진행해도 됨 : False / 멈춰야됨 : True
        print(self.point)
        try:

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            print(new_height, ',', self.last_height)

            if new_height == self.last_height:
                if self.point == 0:
                    # 먹통일 경우 기회를 한번 줘서 올렸다 내리게 하기
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
                    self.driver.implicitly_wait(10)
                    self.cycleScroll()
                    self.point += 1
                    self.end = self.checkHeight()
                    return self.end
                else:
                    self.end = True
                    return self.end
            else:
                # 계속 해도됨
                self.last_height = new_height
                self.end = False
                return self.end
        except Exception as err:
            print(err, '\ncheckHeight',1)
            self.end = True
            return self.end

    def cycleScroll(self):
        self.check += 40
        try:
            # 더보기 버튼 클릭 작업
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # jsdata = yf3HXc;_;$203 YjFXEf;_;$44
            # jscontroller="H6eOGe" jsmodel="y8Aajc"
            element = self.driver.find_element_by_css_selector('.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ')
            self.check += 40
            element.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(10)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[jsdata='yf3HXc;_;${} YjFXEf;_;$44']".format(self.check-1))))


        except selenium.common.exceptions.NoSuchElementException as err:
            # 더보기 버튼이 없을 시 스크롤 작업
            print(err)
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[jsdata='yf3HXc;_;${} YjFXEf;_;$44']".format(self.check-1))))
                return False
            except selenium.common.exceptions.NoSuchElementException as err:
                pass
            except Exception as err:
                print('no find element', err,1)
                return True

        except Exception as err:
            print(err)
            return True

    def deleteElement(self):

        print('deleteElement')
        print(self.delck)
        for i in count(self.delck):
            try:
                # yf3HXc;_;$3 YjFXEf;_;$2
                # yf3HXc;_;$43 YjFXEf;_;$44
                element = self.driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;${} YjFXEf;_;$44"]'.format(i))
                self.driver.execute_script("""
                                var element = arguments[0];
                                element.parentNode.removeChild(element);
                                """, element)
                self.driver.implicitly_wait(2)
            except selenium.common.exceptions.NoSuchElementException as err:
                print(err)
                self.delck = i
                break


    def firstProcess(self):
        self.savefile()
        self.firstDelete()
        # 42
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.driver.implicitly_wait(3)
        self.savefile()
        element = self.driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;$43 YjFXEf;_;$44"]')
        self.driver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, element)
        self.driver.implicitly_wait(2)
        for i in count(45):
            try:
                # yf3HXc;_;$3 YjFXEf;_;$2
                # yf3HXc;_;$43 YjFXEf;_;$44
                element = self.driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;${} YjFXEf;_;$44"]'.format(i))
                self.driver.execute_script("""
                                var element = arguments[0];
                                element.parentNode.removeChild(element);
                                """, element)
                self.driver.implicitly_wait(2)
            except selenium.common.exceptions.NoSuchElementException as err:
                print(err)
                break
        # for
        # 83
        self.driver.execute_script("window.scrollTo(0,0);")
    def firstDelete(self):
        print('deleteElement')
        for i in count(3):
            try:
                # yf3HXc;_;$3 YjFXEf;_;$2
                # yf3HXc;_;$43 YjFXEf;_;$44
                element = self.driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;${} YjFXEf;_;$2"]'.format(i))
                self.driver.execute_script("""
                                var element = arguments[0];
                                element.parentNode.removeChild(element);
                                """, element)
                self.driver.implicitly_wait(2)
            except selenium.common.exceptions.NoSuchElementException as err:
                print(err)
                break
        # for


    def savefile(self):
        page = self.driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        lists = soup.select('div[jsmodel=y8Aajc]')

        with open(file='concat_data/brawlstarz_review_soup_{}.csv'.format(self.filenum), mode='w', encoding='utf-8') as file:
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
        self.filenum += 1 # 다음 작업을 위해 플러스


    def __del__(self):
        self.driver.quit()