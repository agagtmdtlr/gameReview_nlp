from bs4 import BeautifulSoup
import html
import pandas as pd
import os
# from pk
from bs4 import BeautifulSoup
filename = '../concat_data/version_1.02_02.txt'

print(f'file size is {os.stat(filename).st_size/(1024**2)}MB')

txt_file = open(filename,encoding='utf-8')
count = 0
strings = ''
for line in txt_file:
    strings += line
    count +=1
print(count)
txt_file.close()
print(len(strings))
lists = strings.split('<div jscontroller="H6eOGe"')
print(len(lists))
print(lists[0])
final_list = []
for x in lists[1:]:
    strings = '<div jscontroller="H6eOGe" '+x
    soup = BeautifulSoup(strings,'html.parser')
    print(type(soup))
    # print(soup)
    item = soup.select_one('div[jsmodel=y8Aajc]')
    score = item.select_one('div[class=pf5lIe]').select_one('div')['aria-label']
    score = score[3][0]
    day = item.select_one('span[class=p2TkOb]').text
    dates = day.split()
    year = dates[0][:len(dates[0])-1]
    month = dates[1][:len(dates[1])-1]
    day = dates[2][:len(dates[2])-1]
    text = item.select_one('span[jsname=bN97Pc]').text
    text2 = item.select_one('span[jsname=fbQN7e]').text
    if len(text2) == 0:
        final = text
    else:
        final = text2
    final_list.append([score,year,month,day,final])

myframe = pd.DataFrame(data=final_list,columns=['score','year','month','day','text'])

myframe.to_csv('concat_data/google_data.csv')