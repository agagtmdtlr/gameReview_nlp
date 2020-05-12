from gensim.models import word2vec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# 모델 만들기

myframe = pd.read_csv('review_sentence_csv_v03.csv')
score_5 = myframe.loc[myframe['score']==3,'sentence']
print(score_5)
sentence_list = []
for text in score_5:
    print(text)
    imsi = text.split(' ')
    sentence_list.append(imsi)

model = word2vec.Word2Vec(sentence_list, size=200,window=10,min_count=1, hs=1, sg=1)
print(type(model))

model_filename = 'review_model_score/review_model_score3.model'
model.save(model_filename)
print(model_filename + ' 파일 저장됨')
print('finished')



