import re
import string
import pandas as pd
import numpy as np

from wordcloud import STOPWORDS
from nltk.tokenize import TreebankWordTokenizer
from konlpy.tag import Komoran,Kkma,Okt,Hannanum,Mecab,Twitter

myframe = pd.read_csv('concat_data/updatae_csv.csv')

# tag 별 토큰화 비교를 위해 tokenizer 생성
komoran = Komoran()
kkma = Kkma()
okt = Okt()
hananum = Hannanum()
twit = Twitter()
########################
# mecab = Mecab()
#######################################################################
# nltk_tokenizer
# tokenizer = TreebankWordTokenizer()
# stopword = set(STOPWORDS) # 불용어 집합 테스트용
# review = myframe['text'][0]
#
# tokens = komoran.pos(review)
#
# token_list = set([ x[0] for x in tokens if x[1] in ('NNG','NNP')])
# print(token_list)
# print(tokenizer.tokenize(review))
#######################################################################
regex1 = '^[\d가-힣a-zA-Z]*$'
regex2 = '^[\d]*$'
pattern1 = re.compile(regex1)
pattern2 = re.compile(regex2)


# 한글 불용어 집합
hangul_stopword = [ x.strip() for x in open('concat_data/hangle_stop_word.txt','r',encoding='utf-8').readlines()]

token_set = set()
token_dict = dict()
print(string.punctuation)  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
pt = re.compile("!\"#")
pattern = re.compile('[\U00010000-\U0010ffff]',flags=re.UNICODE)
frame_list = []
sentens_list = []
update_id = 1 # 토큰의 집합 분류
noun_set = set()
for idx in range(0,61):
    review = myframe['text'][idx]
    review = pattern.sub(r' ',review)
    tokens = okt.pos(review,norm=True)
    # 불용어 처리
    # 1차 filter \u3000,\xa0 지우기
    # 2차 filter string.punctuation에 해당 되는 단어 지우기
    # 3차 명사 품사만 가져오기
    [noun_set.add(x[0]) for x in tokens if x[1] in ['Noun'] and len(x[1].strip())>1]
    tokens = [ x[0].replace(u'\u3000',u' ').replace(u'\xa0',u' ').
                   translate(str.maketrans('', '', string.punctuation)) for x in tokens if x[1] in ['Noun','Adjective','Verb','Unknown']
               and x not in hangul_stopword]
    # 중복되는 단어 set으로 거르기
    # tokens = [ x for x in tokens if len(x) >1]
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
        one_frame = pd.DataFrame([sentens],columns=['word'])
        # 날짜 추가 ( 각 토큰에 날짜 ) -> daframe : year,month,day
        one_frame['year'] = myframe['year'][idx]
        one_frame['month'] = myframe['month'][idx]
        one_frame['day'] = myframe['day'][idx]
        one_frame['update_id'] = update_id
        frame_list.append(one_frame)
        update_id += 1 # 저장하기
    print(idx,tokens)
############################################# review_tokenSet.csv 저장 ###
with open('update_data/noun_list.txt','w',encoding='utf-8') as file:
    file.write(','.join(noun_set))
# 불용어 탐색
print(len(token_set))
pat = re.compile('^[\d\r가-힣]*$') # 유의미한 글자로 구성되어 있는지 확인, 숫자와 한글로만 구성된 단어
bul = [x for x in token_set if not pat.match(x) or len(x)==1]
print(bul)

with open('update_data/update_sentences.prepro','wt',encoding='utf-8') as file:
    file.write('\n'.join(sentens_list))
# 리뷰 말뭉치 저장
set_frame = pd.DataFrame(token_set,columns=['word'])
set_frame.to_csv('update_data/update_tokenSet_v02.csv')
############################################ update_word_csv.csv 저장 ###
newframe = pd.DataFrame()
for one_df in frame_list:
    newframe = pd.concat([newframe,one_df],ignore_index=True)
print(newframe)
newframe = pd.DataFrame(newframe,columns=['update_id','year','month','day','word'])
newframe.to_csv('update_data/update_word_csv_v02.csv')
# 불용어가 있으면 리스트에 내용 확인 할수 있음

#


# print(string.punctuation)
# print(string.ascii_letters)
# ['※', '&', '!', "'", ')', '–', '-', '=', 'i', '(', '.', 'ㄴ', '☞', '~', '·', 'ㅁ', 'ㄹ', ':', '/', 'P', ',', '%', '"', '→']
# ['4월\xa0밸런스', '매', '얻고\u3000\xa0', '스테이지\u3000·', '그랩,', '힘', '넘', '3초\xa0→', "30초'\xa0게", "증가\xa0'3\xa0→",
#  '·\xa0업데이트', '돕', "%'-", '모드와\xa0새로운', '‘1.6초', '모델\xa0(특수', '회전기\u3000\u3000회전하', "50'\u3000커브볼(스타",
#  '승리\xa0', '램프\u3000\u3000주위', '폭풍\u3000\u300012초', '‘300', '스니커즈\u3000\u3000발', '증가\xa0‘4,600', '150\xa0트로피',
#  '쉘리\u3000쉘', '질주\u3000\u3000리코', '·\xa0미스터', '폭풍이\xa0아군', '–', '피루엣\u3000\u3000특수', '끊', '5초’-', '새', '·\xa0희귀',
#  '수정\u3000·', '엠즈\u3000후원', '상점\u3000·', '기준으로\xa0매치메이킹', '·\xa0재키\xa0-', '변경\u3000특수', '프랭크\u3000노이즈', '별',
#  '700’-', '틱\u3000미니', '휘', '수정\u3000·\xa0새로운', '페니\u3000약탈', "'1840\xa0→\xa0", "'640\xa0→", '자세(스타', '포크아웃\u3000·',
#  "'70\xa0→", '그랩(스타', '증폭\u3000\u3000특수', '요', '지역\u3000·', '길', '선', '0초’\u3000오토매틱', '29일(화)부터', '0.3초',
#  '보석\xa0\u3000\xa0에이전트', '증가\xa0‘40', '타', "'3500\xa0→", '테마\u3000·', '보석\xa0\u3000\xa0늑대', '로사의\xa0몸',
#  "'260\xa0→", "'420\xa0→", '25%’-', '‘100%', '0.5개', '은신술\u3000\u3000은신', "'240\xa0→", '리모델링\u3000·\xa0페니',
#  '내역\u3000·\xa0모티스', '600’\u3000그림자', '-\xa0모티스\u3000전속력', '얻고\xa0', '‘8%', '‘격려', '잃', '시\xa0재장전',
#  '곁', '론', '하이스트\u3000\u3000삭제', '·\xa08비트\xa0-', '5월\xa0밸런스', '프랭크\u3000파워', '수정\u3000·\xa0바운티', '→',
#  '지뢰\u3000\u3000지면', '·\xa0니타\xa0-', '파이퍼\u3000팡팡팡(특수', '리코\u3000통통탄(일반', '브롤러\u3000\u3000로사',
#  '3,200’\xa0오류', '(빅', '피루엣(스타', '0.5초', '밸런스\xa0-', '감소\xa0‘5,500\xa0→', '에', '1,000’-\xa0대릴\u3000강철',
#

print('finished')