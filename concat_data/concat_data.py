import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import DataFrame as df
from pandas import *
google = pd.read_csv('brawlstarz_review_google.csv',header=0)
print(google)


google.columns = ['score','year','month','day','text']
# print(google.columns)
# print(google)
# g_date = google.groupby(by=['year','month'])['text'].count()
# print(g_date)

# g_date.plot(kind='barh')
# plt.show()

g_date_score = google.groupby(by=['year','month'])['score'].mean()
g_date_score = google.pipe(df.groupby,by=['year','month'])['score'].mean()
print(g_date_score)
# g_date_score.plot(kind='barh')
# plt.show()
print(len(g_date_score),g_date_score.max(),g_date_score.min())
print(g_date_score.describe())

print(np.arange(124).reshape(2,-1))
