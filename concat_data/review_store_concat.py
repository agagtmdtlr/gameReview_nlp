import pandas as pd
import numpy as np

google = pd.read_csv('google_data.csv',index_col=0)
apple = pd.read_csv('apple_data.csv', index_col=0)

google['store'] = '구글'
print(len(google))
apple = apple[apple['store']=='애플']

newframe = pd.concat([apple,google],ignore_index=True)
print(len(newframe))
newframe['month'] = newframe['month'].apply(func=lambda x:str(x).zfill(2))
newframe['day'] = newframe['day'].apply(func=lambda x:str(x).zfill(2))


newframe = pd.DataFrame(newframe,columns=['score','store','year','month','day','text'])

newframe.to_csv('review_concat_csv.csv')
