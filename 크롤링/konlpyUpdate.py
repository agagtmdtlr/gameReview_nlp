import pandas as pd
import numpy as np
from nltk.tokenize import TreebankWordTokenizer
import string
from konlpy.tag import Komoran,Kkma,Okt,Hannanum,Mecab,Twitter
from wordcloud import STOPWORDS
myframe = pd.read_csv('../concat_data/updatae_csv.csv')
komoran = Komoran()
tokenizer = TreebankWordTokenizer()
stopword = set(STOPWORDS)
review = myframe['text'][0]

tokens = komoran.pos(review)

token_list = set([ x[0] for x in tokens if x[1] in ('NNG','NNP')])

# print(token_list)
# print(tokenizer.tokenize(review))
import re
regex1 = '^[\d가-힣a-zA-Z]*$'
regex2 = '^[\d]*$'
pattern1 = re.compile(regex1)
pattern2 = re.compile(regex2)
token_set = set()
# for idx in range(0,61):
#     review = myframe['text'][idx]
#     review = review.replace(u'\\xa0','')
#
#     # review = review.replace(u'\\n','').encode('utf-8')
#     tknize = tokenizer.tokenize(review)
#
#
#     tknize_st = [x for x in tknize if pattern1.match(x) and not x.isnumeric()]
#     print(idx, tknize_st)
#     token_set.update(tknize_st)
# print(token_set)
# print(len(token_set))

kkma = Kkma()
okt = Okt()
hananum = Hannanum()
twit = Twitter()
# mecab = Mecab()

hangul_stopword = [x.strip() for x in open('../concat_data/hangle_stop_word.txt', 'r', encoding='utf-8').readlines()]

token_set = set()
print(string.punctuation)  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
pt = re.compile("!\"#")
pattern = re.compile('[\U00010000-\U0010ffff]',flags=re.UNICODE)
for idx in range(0,61):
    review = myframe['text'][idx]
    review = pattern.sub(r' ',review)
    tokens = twit.pos(review,norm=True)
    # 불용어 처리
    tokens = [ x[0].replace(u'\u3000',u' ').replace(u'\xa0',u' ').translate(str.maketrans('', '', string.punctuation)) for x in tokens if x not in hangul_stopword]
    tokens = [ x for x in tokens if len(x)>1]
    token_set.update(tokens)
    print(idx,tokens)

print(len(token_set))
pat = re.compile('^[\d\r가-힣]*$')
bul = [x for x in token_set if not pat.match(x) or len(x)==1]
print(bul)


print(string.punctuation)
print(string.ascii_letters)
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