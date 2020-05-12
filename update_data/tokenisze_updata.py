import re
import string
import pandas as pd
import numpy as np

from wordcloud import STOPWORDS
from nltk.tokenize import TreebankWordTokenizer
from konlpy.tag import Komoran,Kkma,Okt,Hannanum,Mecab,Twitter

myframe = pd.read_csv('updatae_csv.csv')

# tag 별 토큰화 비교를 위해 tokenizer 생성
komoran = Komoran()
kkma = Kkma()
okt = Okt()
hananum = Hannanum()
twit = Twitter()

regex1 = '^[\d가-힣a-zA-Z]*$'
regex2 = '^[\d]*$'
pattern1 = re.compile(regex1)
pattern2 = re.compile(regex2)


# 한글 불용어 집합
hangul_stopword = [ x.strip() for x in open('hangle_stop_word.txt','r',encoding='utf-8').readlines()]

token_set = set()
token_dict = dict()
pt = re.compile("!\"#")
pattern = re.compile('[\U00010000-\U0010ffff]',flags=re.UNICODE)
frame_list = []
sentens_list = []
update_id = 1 # 토큰의 집합 분류
for idx in range(0,61):
    review = myframe['text'][idx]
    review = pattern.sub(r' ',review)
    tokens = okt.pos(review,norm=True)
    # 불용어 처리
    # 1차 filter \u3000,\xa0 지우기
    # 2차 filter string.punctuation에 해당 되는 단어 지우기
    # 3차 명사 품사만 가져오기
    tokens = [ x[0].replace(u'\u3000',u' ').replace(u'\xa0',u' ').translate(str.maketrans('', '', string.punctuation)) for x in tokens if x[1] in ['Noun'] and x not in hangul_stopword]
    # 중복되는 단어 set으로 거르기
    tokens = [ x for x in tokens if len(x) >1]
    sentens = ' '.join(tokens)
    sentens_list.append(sentens)
    tokens = set(tokens)

    # 총단어사전(set)에 추가하기
    token_set.update(tokens)
    # 업데이트별 사전 (idx 기준:시간순)에 추가하기
    token_dict[idx] = tokens
    # 각업데이트별 데이터프레임화 하여 나중여 concat에 사용
    # dataframe  1 row : tokens,year,month,day
    if len(token_set) != 0:
        strings = ','.join(tokens)
        one_frame = pd.DataFrame([strings],columns=['word'])
        # 날짜 추가 ( 각 토큰에 날짜 ) -> daframe : year,month,day
        one_frame['year'] = myframe['year'][idx]
        one_frame['month'] = myframe['month'][idx]
        one_frame['day'] = myframe['day'][idx]
        one_frame['update_id'] = update_id
        one_frame['ti']
        frame_list.append(one_frame)
        update_id += 1 # 저장하기
    print(idx,tokens)
############################################# review_tokenSet.csv 저장 ###
# 불용어 탐색
print(len(token_set))
pat = re.compile('^[\d\r가-힣]*$') # 유의미한 글자로 구성되어 있는지 확인, 숫자와 한글로만 구성된 단어
bul = [x for x in token_set if not pat.match(x) or len(x)==1]
print(bul)

# with open('update_sentences.prepro','wt',encoding='utf-8') as file:
#     file.write('\n'.join(sentens_list))
# # 리뷰 말뭉치 저장
# set_frame = pd.DataFrame(token_set,columns=['word'])
# set_frame.to_csv('update_tokenSet_v02.csv')
############################################ update_word_csv.csv 저장 ###
newframe = pd.DataFrame()
for one_df in frame_list:
    newframe = pd.concat([newframe,one_df],ignore_index=True)
print(newframe)
newframe = pd.DataFrame(newframe,columns=['update_id','year','month','day','word'])
newframe.to_csv('update_word_csv_v03.csv')
# 불용어가 있으면 리스트에 내용 확인 할수 있음


print('finished')