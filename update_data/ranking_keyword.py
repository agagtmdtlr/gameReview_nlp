import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename = 'update_keyword_by_similar_matrix.csv'
keywordFrame = pd.read_csv(filename,index_col=0)
key_rank_list = []
for x in range(0,61):
    rank = list(keywordFrame[str(x)].sort_values(axis=0,ascending=False)[:10].index)
    key_rank_list.append(rank)

columns = [str(x)+'위' for x in range(1,11)]
indexs = [x for x in range(1,62)]

rankFrame = pd.DataFrame(key_rank_list,columns=columns,index=indexs)
rankFrame.to_csv('update_keyword_top10.csv')

df = pd.read_csv('update_word_csv_v03.csv',index_col=0)
