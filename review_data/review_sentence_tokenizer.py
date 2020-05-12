from konlpy.tag import Okt
from nltk.tokenize import sent_tokenize
import nltk
import pandas as pd

import re
import string
import pandas as pd
import numpy as np

from wordcloud import STOPWORDS
from nltk.tokenize import TreebankWordTokenizer
from konlpy.tag import Komoran,Kkma,Okt,Hannanum,Mecab,Twitter

# nltk.download('punkt')

frame_list = []
lineSentence_list = []
token_set = set()


myframe = pd.read_csv('review_concat_csv02.csv',index_col=0)
imo_pattern = re.compile('[\U00010000-\U0010ffff]',flags=re.UNICODE)
okt = Okt()
hangul_stopword = [ x.strip() for x in open('hangle_stop_word.txt','r',encoding='utf-8').readlines()]
# nltk.download('punkt')
total_len = 0
for idx in range(42995):
    # 문장 분류 리스트
    text = myframe['text'][idx]
    review_id = idx
    sent_list = sent_tokenize(text)
    # 문장 만다 단어 토큰화
    one_review_sentence_list = []
    for sent in sent_list:
        # 토큰화 불가능한 이모티콘 제거
        sent = imo_pattern.sub(r' ',sent)
        tokens = okt.pos(sent,norm=True)
        # 불용어 처리
        # tokens : list()
        tokens = [x[0].
                      replace(u'\u3000', u' ').
                      replace(u'\xa0', u' ').
                      translate(str.maketrans('', '', string.punctuation))
                  for x in tokens
                  if
                  x[1] in ('Noun')
                  and
                  x[0] not in hangul_stopword
                  and
                  len(x[0]) > 1]
        # 컨테이너에 담기
        if len(tokens) != 0:
            sentence = ' '.join(tokens)
            one_review_sentence_list.append([review_id, myframe['year'][idx],myframe['month'][idx],myframe['day'][idx],myframe['score'][idx],sentence])
        # lineSentence_list.append(sentence) # for review_sentences.prepro
        # token_set.update(tokens) # for review_tokenSet_sentence.csv
        # if len(tokens) != 0:
        #     one_frame = pd.DataFrame(tokens, columns=['word'])
        #     # 날짜 추가 ( 각 토큰에 날짜 ) -> daframe : year,month,day
        #     one_frame['year'] = myframe['year'][idx]
        #     one_frame['month'] = myframe['month'][idx]
        #     one_frame['day'] = myframe['day'][idx]
        #     one_frame['store'] = myframe['store'][idx]
        #     one_frame['score'] = myframe['score'][idx]
        #     one_frame['review_id'] = review_id
        #     frame_list.append(one_frame)
        print(idx, tokens)
    one_frame = pd.DataFrame(one_review_sentence_list,columns=['review_id','year','month','day','score','sentence'])
    frame_list.append(one_frame)

### 파일 저장 #####
############################################################################
# with open('review_linesentences.prepro','w',encoding='utf-8') as file:
#     file.write('\n'.join(lineSentence_list))
#
# setframe = pd.DataFrame(token_set,columns=['word'])
# setframe.to_csv('review_tokenSet_sentence.csv')
#
# newframe = pd.DataFrame(columns=['word','year','month','day','store','score','review_id'])
# for frame in frame_list:
#     newframe = pd.concat([newframe,frame],ignore_index=True)
# newframe.to_csv('review_word_csv_v03.csv')
# # print(total_len)

newframe = pd.DataFrame(columns=['review_id','year','month','day','score','sentence'])
for frame in frame_list:
    newframe = pd.concat([newframe,frame],ignore_index=True)
newframe.to_csv('review_sentence_csv_v03.csv')
############################################################