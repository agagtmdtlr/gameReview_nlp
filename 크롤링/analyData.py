import pandas as pd
import numpy as np
myframe = pd.read_csv('../concat_data/review_concat_csv.csv', index_col=0)

print(len(myframe))
myframe['lens'] = myframe['text'].apply(func=lambda x:'ok'if len(x)>=20 else np.nan)
myframe.dropna(subset=['lens'],inplace=True )
print(len(myframe))
mygrounping = myframe.groupby(['year','month'])['day']
data = mygrounping.count()
print(data)

mygrounping = myframe.groupby(['score'])['day']
data = mygrounping.count()
print(data)

mygrounping = myframe.groupby(['score','year','month'])['day']
data = mygrounping.count()
print(data)



import matplotlib.pyplot as plt
#
# if isinstance(concat_data,pd.Series):
#     concat_data.plot(kind='bar')
#     plt.show()

# for i in range(1,6):
