import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


similar_filename = 'update_similarity_matrix.csv'
sentence_filename = 'update_word_csv_v02.csv'
one_hot_filename = 'update_tokenSet_v02.csv'

similarFrame = pd.read_csv(similar_filename,index_col=0)
sentenceFrame = pd.read_csv(sentence_filename)
one_hot_list = list(pd.read_csv(one_hot_filename)['word'])

frame_list = [] # elemnet (update_id,one_frame)
# one_hot_encoding
for update_id in range(1,62):
    one_hot_dict = {x: 0 for x in one_hot_list} # 초기는 모두 0으로 초기화
    word_series = sentenceFrame.loc[sentenceFrame.update_id == update_id,'word']
    for word in word_series:
        one_hot_dict[word] = 1 # 단어가 존재하니 1로 변경
    one_frmae = pd.DataFrame(one_hot_dict,index=[update_id])
    frame_list.append(one_frmae)

one_hot_frame = pd.DataFrame(columns=one_hot_list)
for x in frame_list:
    one_hot_frame = pd.concat([one_hot_frame,x])
print(one_hot_frame.T)

result = np.dot(similarFrame,one_hot_frame.T)
key_word = pd.DataFrame(result,index=one_hot_list)
print(key_word)

one_hot_frame.to_csv('update_onehotencoding.csv')
key_word.to_csv('update_keyword_by_similar_matrix.csv')
# for x in similarFrame.items():
#     print(x)
# print(key_word[0].sort_index())