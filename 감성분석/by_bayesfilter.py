import os, sys, math
from konlpy.tag import Okt
import pandas as pd

class BayesFilter:
    def __init__(self):
        self.filename = 'review_concat_csv02.csv'
        self.data_frame = pd.read_csv(self.filename, encoding='utf-8')
        self.words = set()
        self.word_dic = {}
        self.category_dic = {}

    def fit(self, text, category):
        self.incWord(text,category)
        self.incCategory(category)

    def incWord(self, text,category):
        twitter = Okt()
        malist = twitter.pos(text,norm=True)

        if category not in self.word_dic:
            self.word_dic[category] = {}

            for word in malist:
                if word[1] not in ["Josa","Eomi","Punctuation"]:
                    if word not in self.word_dic[category]:
                        self.word_dic[category][word[0]] = 0
                        self.word_dic[category][word[0]]+=1
                        self.words.add(word[0])

    def incCategory(self,category):
        if category not in self.category_dic:
            self.category_dic[category] = 0
            self.category_dic[category] +=1

    def word_prob(self, word,category):
        if word not in self.word_dic[category]:
            n = 0
        else:
            n = self.word_dic[category][word]

        return math.log(n+1 / (len(self.words)+sum(self.word_dic[category].values())))

    def category_prob(self, category):
        return math.log(self.category_dic[category] /sum(self.category_dic.values()))

    def predict(self, text):
        maxScore = -sys.maxsize

        for category in self.category_dic.keys():
            score = 0
            categoryScore = self.category_prob(category)
            score += categoryScore
            twitter = Okt()
            malist = twitter.pos(text,norm = True)

            for word in malist:
                score += self.word_prob(word[0], category)

                if maxScore < score:
                    bestCategory = category
                    maxScore = score

        return bestCategory

# from vayse import BayesFilter

vy = BayesFilter()

print(vy.data_frame)
negative = vy.data_frame[vy.data_frame['score'] == 1]['text']

cnt = 0

neg_str = ''

for review in negative :
    neg_str += review
    # vy.fit(review, '부정')
    # print(review)

    cnt += 1
    print(cnt)
    if cnt >= 200:
        break

vy.fit(neg_str, '부정')

vy.fit('킹갓 브롤스타즈정말 갓겜입니다 굿굿 재미있어요굿', '긍정')

result = vy.predict("123,5,애플,2019,12,16,갓겜👍👍👍👍👍👍👍👍👍👍👍👍👍이 게임 너무 재미있는데 솔직히 말해 PC 버전을 출시하면 좋을 것 같습니다. STEAM 런쳐를 통해 플레이할 수 있으면 좋을 것 같아요. 그리고 하나 더. 일부 디바이스 에서 업데이트를 하지 못하는 문제가 있습니다. 어쟀든간에 이 오류 수정하면 좋을 것 같습니다. 왜냐하면 업뎃을 안하면 실행이 안되요.")
print(result)


result = vy.predict("재미있어요굿")
print(result)

result = vy.predict("정말 좋아요 근데.....제목대로 브롤은 정말 갓겜이에여")
print(result)

result = vy.predict('개짜증나')
print(result)

print(vy.category_dic)
print(vy.word_dic)
