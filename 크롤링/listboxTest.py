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
driver.get(url)

body = driver.find_element_by_css_selector('body')
# listbox = body.find_element_by_css_selector('.jgvuAb.gRsdLe')
# print(listbox)
# listbox.click()
# option = listbox.find_element_by_css_selector('.MocG8c.UFSXYb.LMgvRb[concat_data-value="2"]')
# option.click()
action = "click:cOuCgd(LgbsSe); keydown:I481le; keypress:Kr2w4b;"
action += " mousedown:UX7yZ(LgbsSe),npT2md(preventDefault=true); mouseup:lbsD7e(LgbsSe); mouseleave:JywGue;"
action += " touchstart:p6p2H(LgbsSe); touchmove:FwuNnf; touchend:yfqBxc(LgbsSe|preventMouseEvents=true|preventDefault=true);"
action += " touchcancel:JMtRjd(LgbsSe); focus:AHmuwe; blur:O22p3e;b5SvAb:TvD9Pc;"


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

print(By.CSS_SELECTOR)
# try:
#     element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MocG8c.UFSXYb.LMgvRb[concat_data-value='2']")))
#     print(type(element))
#     element.click()
# finally:
#     driver.quit()

from selenium.webdriver.common.action_chains import ActionChains

# menu = driver.find_element_by_css_selector(".nav")
# hidden_submenu = driver.find_element_by_css_selector(".nav #submenu1")
#
# actions = ActionChains(driver)
# actions.move_to_element(menu)
# actions.click(hidden_submenu)
# actions.perform()

listbox = body.find_element_by_css_selector('.jgvuAb.gRsdLe')
# option = listbox.find_element_by_css_selector('.MocG8c.UFSXYb.LMgvRb[concat_data-value="2"]')
# actions = ActionChains(driver)
# actions.move_to_element(listbox)
# actions.click(option)
# actions.perform()

# driver.execute_script("arguments[0].setAttribute('class','vote-link up voted')", element) 값 밖기
# driver.execute_script("arguments[0].setAttribute('aria-selected','true')")
listbox = body.find_element_by_css_selector('.MocG8c.UFSXYb.LMgvRb.KKjvXb[concat_data-value="1"]')
listbox.click()
option = body.find_element_by_css_selector('.MocG8c.UFSXYb.LMgvRb[concat_data-value="2"]')
driver.execute_script("arguments[0].setAttribute('aria-selected','false')", listbox)
driver.execute_script("arguments[0].setAttribute('aria-selected','true')", option)
print(option.text)
# option.click()
print('작동완료')

html = driver.execute_script("return document.documentElement.outerHTML")
element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,".MocG8c.UFSXYb.LMgvRb[concat_data-value='2'']")))