import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

plt.rc('font', family='Malgun Gothic')

filename = 'update_word_csv_v04.csv'
forFrame = pd.read_csv(filename,index_col=0,usecols=['update_id','year','month','day'])
# print(forFrame)
forFrame['fd'] = forFrame['year'].apply(lambda x : str(x))
forFrame['fd'] += forFrame['month'].apply(lambda x : '-'+str(x))
forFrame['fd'] += forFrame['day'].apply(lambda x : '-'+str(x))
print(forFrame['fd'])
seri_list = []
percent_list = []
# 업데이트별 반응
for row in forFrame.iterrows():
    frame = pd.read_csv(f'update_id{row[0]}_{row[1][0]}_{row[1][1]}_{row[1][2]}.csv',index_col=0)
    mygrouping = frame.groupby(by='LABEL')['LABEL']
    data=mygrouping.count()
    total = sum(data.values)
    percent = [x/total*100 for x in data.values]
    seri_list.append(data.values)
    percent_list.append(percent)


# 개수 리뷰 그래프
df = pd.DataFrame(seri_list,index=forFrame['fd'],columns=['긍정','복합','부정'])


df.plot(kind='barh',figsize=(10,10))
plt.title('업데이트별 리뷰 반응')
plt.ylabel('업데이트 일자')
plt.xlabel('리뷰 개수')

plt.figure()

# 퍼센트 리뷰 그래프
df2 = pd.DataFrame(percent_list,index=forFrame['fd'],columns=['긍정','복합','부정'])

avg_negative = df2['부정'].mean()
df2.plot(kind='bar',figsize=(15,10),rot=45)
plt.title('업데이트별 리뷰 반응')
plt.xlabel('업데이트 일자')
plt.ylabel('퍼센트')
plt.axhline(avg_negative)
plt.show()
