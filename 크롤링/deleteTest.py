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

start = 243

# for i in count(3):
#     try:
#         element = driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;${} YjFXEf;_;$2"]'.format(i))
#         driver.execute_script("""
#             var element = arguments[0];
#             element.parentNode.removeChild(element);
#             """, element)
#     except selenium.common.exceptions.NoSuchElementException as err :
#         print(err)
#         break



driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.implicitly_wait(3)

element = driver.find_element_by_css_selector('div[jsdata="yf3HXc;_;$3 YjFXEf;_;$2"]')
driver.execute_script("""
             var element = arguments[0];
             element.parentNode.removeChild(element);
             """, element)