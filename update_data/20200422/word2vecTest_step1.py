from bs4 import BeautifulSoup
from konlpy.tag import Okt
from gensim.models import word2vec
# import smart_open.gcs
import pandas as pd


noun_list = open('update_data/noun_list.txt','r',encoding='utf-8').read().split(',')



result_file = 'update_data/update_sentences.prepro'

# 모델 만들기
sentence = word2vec.LineSentence(source=result_file)
print(type(sentence))

model = word2vec.Word2Vec(sentence, size=200,window=10, hs=1, min_count=2, sg=1)
print(type(model))
print(model)
model_filename = 'update_data/model_20200421.model'
model.save(model_filename)
print(model_filename + ' 파일 저장됨')
print('finished')
print(len(model.wv.vocab))
stopword = ['정수정','감','소량','롤링','로드','에고','유성','러시','매직','오라','수정','조정','문제','감소','밸런스','의견','여러분','대한']
wv = model.wv.vocab
simi_key = [x for x in wv.keys() if x in noun_list and x not in stopword and len(x) >= 2]
print(len(simi_key)) #800
simi_list = []
print(type(model))

for m in simi_key:
    simi_dict = {x: 0 for x in simi_key}
    simi = model.wv.most_similar(positive=[m],topn=997)

    for i in simi:
        if i[0] in simi:
            simi_dict[i[0]] = i[1]
    simi_dict[m] = 1
    simi_list.append(simi_dict)

simiFrame = pd.DataFrame(simi_list,index=simi_key)


#one_hot_encoding
myframe = pd.read_csv('update_data/update_word_csv_v02.csv',index_col=0)
# one_hot matrix
one_hot_key = simi_key
one_hot_list = []
for data in myframe['word']:
    one_hot_dict = { x:0 for x in one_hot_key}
    data_list = data.split(' ')
    for i in data_list:
        if i in one_hot_dict: one_hot_dict[i] += 1 # 1 encoding
    print(one_hot_dict)
    one_hot_list.append(one_hot_dict)

oneFrame = pd.DataFrame(one_hot_list).T
print(oneFrame.shape)
# print(oneFrame)

import numpy as np

scoreFrame = pd.DataFrame(np.dot(simiFrame,oneFrame),columns=np.arange(1,62),index=simi_key).T
# print(scoreFrame)
row_list = []
for row in scoreFrame.iterrows():
    l = row[1].sort_values(ascending=False)[:10].index
    row_list.append(l)

fdf = pd.DataFrame(row_list,columns=[str(x)+'위' for x in range(1,11)])
print(fdf)