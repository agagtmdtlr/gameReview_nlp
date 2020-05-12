import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

url='https://cafe.naver.com/brawlstars/491712'

# .tbody m-tcol-c
# #tbody
# span

driver = webdriver.Chrome('d:/chromedriver.exe')
driver.get(url)
##############################
# from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
# chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
# chrome = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
# chrome.get('http://stackoverflow.com/')
##########################################################
lists = driver.find_elements_by_css_selector('.tbody.m-tcol-c div')
driver.set_network_conditions()
print(len(lists))