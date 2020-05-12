import numpy as np
import pandas as pd

from konlpy.tag import Okt
from nltk.tokenize import sent_tokenize


df1 = pd.read_csv('update_word_csv_v04.csv',index_col=0)
df2 = pd.read_csv('update_word_csv_v02.csv',index_col=0)
df3 = pd.merge(df2,df1,on='update_id',how='inner')
df3.drop(columns=['year_x','month_x','day_x','word_x'],inplace=True)
df3.columns = ['update_id','year','month','day','word']
print(df3.columns)
print(df3)
df3.to_csv('update_word_csv_v06.csv')
