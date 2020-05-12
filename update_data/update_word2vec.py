from gensim.models import word2vec
from konlpy.tag import _mecab
# 모델 만들기
source = 'update_sentences.prepro'
sentence = word2vec.LineSentence(source=source)
print(type(sentence))
print(sentence.max_sentence_length)

model = word2vec.Word2Vec(sentence, size=200,window=10,min_count=1, hs=1, sg=1)
print(type(model))

model_filename = 'update_model.model'
model.save(model_filename)
print(model_filename + ' 파일 저장됨')
print('finished')

# 저장된 model 파일의 유사도를 이용한 시간화

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rc('font',family='Malgun Gothic')


model_filename = 'update_model.model'
model = word2vec.Word2Vec.load(model_filename)
print(model)
# Word2Vec(vocab=676, size=200, alpha=0.025)
arr = np.array([1 for x in range(40000)]).reshape(200,200)

wordset = pd.read_csv('update_tokenSet_v02.csv')
worde_vec = model.wv
# print(worde_vec.vocab)
vocabs = worde_vec.vocab
# print(worde_vec.most_similar(positive=['공격'],topn=None))
print(type(worde_vec.most_similar(positive=['공격'],topn=1140)))
# print(worde_vec.most_similar(positive=['피해'],topn=1140))
print()

column_dict = dict()
for x in wordset['word']:
    column_dict[x] = list()
index_list = list()
# 단어갯수 * 단어갯수의 유사도 행렬
for key1,word1 in wordset['word'].items():

    imsi_arr = worde_vec.most_similar(positive=[word1],topn=1140)
    for k in imsi_arr:
        column_dict[k[0]].append(k[1])
    column_dict[word1].append(1)
    index_list.append(word1)

print(len(column_dict['카드']))
print(len(index_list))
newframe = pd.DataFrame(column_dict,index=index_list)
print(newframe)

newframe.to_csv('update_similarity_matrix.csv')
# bargraph = model.most_similar(positive=['국민'], topn=10)

