import pandas as pd
import numpy as np
myframe = pd.read_csv('../concat_data/brawlstarz_update_raw_data.csv', index_col=0)

# print(myframe.columns)
print(len(myframe))


yearl = []
monthl = []
dayl = []
def ap(x):
    if isinstance(x,str):
        imsi = x.split()[0]
        dl = imsi.split('.')
    yearl.append(dl[0])
    monthl.append(dl[1])
    dayl.append(dl[2])

myframe['date'].apply(func=ap)

myframe.drop(columns='date')

myframe['year'] = yearl
myframe['month'] =monthl
myframe['day'] = dayl

def conts(x):
    if isinstance(x,str):
        imsi = x.split('주세요.◈ 브롤스타즈(Brawl Stars)')
        print(type(imsi),len(imsi))
        if len(imsi) >=2 :
            imsi = imsi[1]
        else: imsi=x.split('브롤스타즈(Brawl Stars)')[1]
        print(imsi)
        return imsi

myframe['text'] = myframe['contents'].apply(func=conts)
print(len(myframe['text']))

myframe.to_csv('concat_data/updatae_csv.csv')