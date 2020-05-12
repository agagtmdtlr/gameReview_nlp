import pandas as pd
import numpy as np
from gensim.models import word2vec

for num in range(1,5):
    # 상관 행렬
    simiFrame = pd.read_csv('review_similar_matrix_score{}.csv'.format(num),index_col=0)

    # one hot encoding 행렬
    onehotFrame = pd.read_csv('review_one_hot_encoding_score{}.csv'.format(num),index_col=0)

    # 상관 인덱스 : 인덱스 on hot 인덱스 : 컬럼
    indexs = simiFrame.index
    columns = onehotFrame.index

    # 두 행렬 내적
    result= np.dot(simiFrame,onehotFrame.T)

    # 내적 행렬 프레임
    newframe = pd.DataFrame(result,index=indexs,columns=columns)
    newframe = newframe.T
    key_rank_list = []
    # newframe['index'] = newframe.index
    # print(indexs)
    print(newframe)
    cnt = 0
    for x in newframe.iterrows():
        print(type(x),type(x[0]),type(x[1]))
        # print(newframe['19'])
        imsi = x[1]
        # print(imsi)
        dat = imsi.sort_values(axis=0,ascending=False).T[:10].index
        print(dat)
        key_rank_list.append(dat)
        cnt += 1
    columns = [str(x) + '위' for x in range(1, 11)]
    indexs = [x for x in newframe.index]
    rankFrame = pd.DataFrame(key_rank_list, columns=columns, index=indexs)
    rankFrame.to_csv('review_keyword_top10_score{}.csv'.format(num))
