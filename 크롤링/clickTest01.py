import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


url = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&showAllReviews=true'
filepath = 'd:/chromedriver.exe'

driver = webdriver.Chrome(filepath)
request = urllib.request.Request(url)
driver.get(url)

body = driver.find_element_by_css_selector('body')
lists = body.find_elements_by_css_selector('.LkLjZd.ScJHi.OzU4dc')
print(len(lists))
for ele in lists:
    print(type(ele))
    ele.click()