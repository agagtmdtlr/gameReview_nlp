import copy
import time
import selenium.common.exceptions

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = 'https://blog.brawlstars.com/ko/blog/game-updates/page/1/'
path = 'd:/chromedriver.exe'

driver = webdriver.Chrome(path)
driver.get(url)
driver.implicitly_wait(3)
lists = driver.find_elements_by_css_selector('div[class="home-news-primary-item article__shadow "] > a')
for a in lists:
     url = a.get_attribute('href')
     print(url)
     driver.get(url)
     driver.implicitly_wait(3)
time.sleep(5)
driver.quit()