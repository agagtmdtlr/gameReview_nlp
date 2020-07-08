from string import ascii_letters
from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud
from PIL import Image
from wordcloud import ImageColorGenerator
from gensim.models import word2vec
from sklearn.manifold import TSNE


import nltk
import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from konlpy.tag import Okt

'''
불러오는 파일 목록
    update_word_remake.csv : 업데이트 날짜, 업데이트 분류 키워드 항목
    update_review/update_review_YYYY년MM월DD일.csv : 업데이트 기간별 리뷰 데이터
    noun stopword.txt    
    YYYY년MM월DD일_category.txt
    
    
저장하는 파일 목록
'''



plt.rc('font', family='Malgun Gothic')
plt.rcParams["figure.figsize"] = (15,6)

# 감정별 이미지
image_path = {'긍정':'positive.png','부정':'negative.jpg','복합':'middle.png'}

filename = 'update_word_remake.csv'
forFrame = pd.read_csv(filename,index_col=0,usecols=['update_id','year','month','day','word'])

# fd 전체 날짜
forFrame['fd'] = forFrame['year'].apply(lambda x : str(x))
forFrame['fd'] += forFrame['month'].apply(lambda x : '-'+str(x))
forFrame['fd'] += forFrame['day'].apply(lambda x : '-'+str(x))


def analyData(forFrame):
    # 내가 사용할 형태소 분석기 불러오기
    okt = Okt()
    review_dict = {}


    # 불용어 처리
    Stopword = open('noun_stopword.txt','r',encoding='utf-8').read().split(',')
    # 각 업데이트별 데이터 분석
    for itrow in forFrame.iterrows():
        # 해당 업데이트에 관련된 리뷰데이터 파일 불러오기
        reviewframe = pd.read_csv(f'update_review/update_review_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일.csv')

        # 리뷰프레임을 Label로 구별하여 review_dict 사전에 넣기
        # review_dict['긍정'] = reviewframe
        review_dict['긍정'] = reviewframe[reviewframe['LABEL'] =='긍정']
        review_dict['복합'] = reviewframe[reviewframe['LABEL'] == '복합']
        review_dict['부정'] = reviewframe[reviewframe['LABEL'] == '부정']
        # review_dict['긍정'] = pd.concat([review_dict['긍정'],review_dict['복합']])


        # 감정별 데이터 분석
        for label,f in review_dict.items(): # items(감정, 감정 프레임)
            print(label)

            frame_row = []  # 명 : 키워드 , 형: 키워드 , 동 : 키워드

            noun_tokens = set()  # score에 사용할 명사 데이터
            adjec_s = set()
            verb_s = set()
            unk_s = set()
            freq_dict = {}
            all_sentense_list = []

            # 리뷰 개수 설정하기
            item_cnt = 30000
            text_id_list = list(f['ID'][:item_cnt])
            print(text_id_list)
            # 각 감정 프레임에서 리뷰 100개만 형태소 분석기 돌리기
            # 한 리뷰에 해당하는 단어들 집합 넣을 사전 : TDM 행렬을 만드는데 사용
            review_tokens_dict = dict()
            for textid,text in enumerate(f['CONTENTS'][:item_cnt]): # contents iter
                # 해당 리뷰의 토큰은 textid key로 value list에 다 담는다.
                review_tokens_dict[text_id_list[textid]] = list()

                # 리뷰 문자 토큰화
                sent_tokens = sent_tokenize(text)
                # print(sent_tokens)
                # print('sent_l',len(sent_l))


                # 각 문장 토큰 단어 토큰화하기
                for sent_token in sent_tokens:

                    word_tokens = []  # 각 문자의 단어 토큰

                    # okt 형태소 분석기
                    pos = okt.pos(sent_token,norm=True)
                    # print(pos)

                    # 명사,동사,형용사 만 추출하기
                    pos = [x for x in pos
                           if x[0] not in('롤러','지금','다른') and
                           x[1] in ['Noun','Verb','Adjective','Unknown'] and
                           len(x[0])>1]
                    print(pos)
                    # word2vec에 학습시킬 데이터 (명사,형용사,동사)
                    word_tokens.extend([ x[0] for x in pos ])

                    # word2vct 학습후 가중치행렬롤 만든 키워드 ( 명사)
                    noun_tokens.update([ x[0] for x in pos if x[1] in ['Noun'] ]) # 중복제거 있음

                    review_tokens_dict[text_id_list[textid]].extend([ x[0] for x in pos if x[1] in ['Noun'] ]) # 중복제거 없음 : 빈도수 행렬

                    # 학습데이터 집합에 넣기
                    all_sentense_list.append(word_tokens)
                # end Okt 형태소 분석기
            """ 
            end result :
                    all_sentense_list
                    review_tokens_dict
                    noun_tokens
            """
            # end sent_tokenizer 문장 분석기


            # 분류한 토큰으로 word2vec 학습 시키기
            model = word2vec.Word2Vec(all_sentense_list,
                                      size=100,
                                      window=3,
                                      iter=5,
                                      min_count=1,
                                      hs=1,
                                      sg=1,
                                      workers=6)

            # size 100 concat_data dimesion 2로 줄이기
            tsne = TSNE(n_components=2) # 2차원 설정

            # noun_vocab : 학습된 명사 모록
            noun_vocab = [ w for w in model.wv.vocab if w in noun_tokens and w not in Stopword]
            W_data = model.wv[noun_vocab]
            # tsne
            W_tsne = tsne.fit_transform(W_data)

            # 차원 축소한 데이터 dataframe으로 만들기
            tsneFrame = pd.DataFrame(W_tsne,index=noun_vocab,columns=['x','y'])
            tsneFrame.to_csv(f'uclid_data/tsneFrame_{label}.csv')
            # print(tsneFrame)

            ################################
            # plt.figure()
            # # tsne프레임으로 좌표 그리기
            #
            # # fig.set_size_inches(100, 80)
            # # ax = fig.subplots()
            #
            # plt.scatter(tsneFrame['x'], tsneFrame['y'])
            # plt.title(f'{label}의 명사 관계도')
            # for word, pos in tsneFrame.iterrows():
            #     plt.annotate(word, pos, fontsize=5)
            # ### 좌표 그리고 그 표를 파일로 저장하기
            # plt.savefig(f'uclid_data/{label}_noun_scatter.png', dpi=600, bbox_inches='tight')
            ###############################################

            # 거리 행렬 구하기 : noun_vocab * noun_vocab
            # 거리 행렬 프레임 데이터
            data_n = len(noun_vocab)**2
            print('data_n','\n',data_n)
            uclid_data_list = list()

            sum_distance = 0
            for e1,row in tsneFrame.iterrows():
                frame_row_dict = dict()

                mean = 0

                # 기준 단어 좌표
                e1x = row.x
                e1y = row.y

                # 상대 단어 좌표와의 유클리드 거리 계산
                for e2 in noun_vocab:
                    e2x = tsneFrame.loc[e2].x
                    e2y = tsneFrame.loc[e2].y
                    # 유클리드 거리 계산
                    distance = math.sqrt((e1x-e2x)**2+(e1y-e2y)**2)
                    sum_distance += distance
                    frame_row_dict[e2] = distance
                # end row distance calculation
                uclid_data_list.append(frame_row_dict)
            uclidFrame = pd.DataFrame(uclid_data_list,index=noun_vocab)
            uclidFrame.to_csv(f'uclid_data/uclidFrame_{label}.csv')

            mean_distance = sum_distance/data_n

            v = 0

            for idx,row in uclidFrame.iterrows():
                for distance in row:
                    v += (distance - mean_distance)**2

            v = v/data_n

            # var = uclidFrame.var()
            # print('var','\n',var)
            # 가중치 행렬 구하기 : exp(-(거리 제곱)/(2*분산))
            weight_data_list = list()
            for w in noun_vocab:
                one_row_dict = dict()
                #가중치 계산
                # v = var[w]
                for wid,dis in uclidFrame[w].items():
                    weight = math.exp(-(dis**2)/(2*v))
                    one_row_dict[wid] = weight
                weight_data_list.append(one_row_dict)

            weightFrame = pd.DataFrame(weight_data_list,index=noun_vocab)
            weightFrame.to_csv(f'uclid_data/weightFrame_{label}.csv')

            # 가중치 행렬에서 업데이트 관련 키워드만 추출(명사)
            # 실제 채점할 단어 목록 리스트
            # print(list(itrow[1]['word']))
            up_kwd_list = itrow[1]['word'].split(',')
            # up_kwd_list = ['태블릿', '토큰', '조이스틱', '기기',\
            # '매칭', '찾기', '트로피', '오락실', '테이크다운', \
            # '바이러스', '비비', '닌자', '큐피트', '에이전트', \
            # '길거리', '코알라', '히로인', '보석', '핫존', '미스터', '로봇', '깡통', '가방']
            category_noun_list = [w for w in weightFrame.index if w in up_kwd_list]
            # print('category_noun_list',category_noun_list)
            categoryFrame = weightFrame.loc[category_noun_list,:]
            # print('categoryFrame',categoryFrame)



            # TDM 행렬 구하기 : 단어 : 빈도수
            TDM_data_list = []
            for textid,review_token in review_tokens_dict.items():
                one_row_dict = {x:0 for x in noun_vocab}
                for t in review_token:
                    if t in noun_vocab:
                        one_row_dict[t] = one_row_dict[t]+1
                TDM_data_list.append(one_row_dict)

            TdmFrame = pd.DataFrame(TDM_data_list,index = review_tokens_dict.keys()).T
            TdmFrame.to_csv(f'uclid_data/tdmFrame_{label}.csv')

            # print(TdmFrame)

            score_arr = np.dot(categoryFrame,TdmFrame)

            # print('score_arr',score_arr)
            scoreFrame = pd.DataFrame(score_arr,index=category_noun_list,columns=review_tokens_dict.keys())
            # print(scoreFrame)
            scoreFrame.to_csv(f'uclid_data/scoreFrame_{label}.csv')
            # print(scoreFrame)
            # 분류된 단어 리스트
            top_word_list = []
            for textid, row in scoreFrame.T.iterrows():
                sort_key = row.sort_values(ascending=False)[:1].index
                # print(sort_key)
                top_word_list.append(list(sort_key)[0])
            print(top_word_list)
            # 분류된 단어 목록 파일에 저장
            with open(f'top_word_list_{label}.txt','w',encoding='utf-8') as file:
                file.write(','.join(top_word_list))

            # 분류된 단어가 속한 카테고리로 카운트:
            # txt file format
            # category1:kwd1,kwd2,kwd3....
            # category2:kwd1,kwd2,kwd3....
            imsi_list = [x.strip() for x in open(f'reference_category/{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_category.txt', 'r', encoding='utf-8').readlines()]
            # 카테고리별 단어 집합 사전

            Category_dict = {i.split(':')[0]: i.split(':')[1].split(',') for i in imsi_list}
            Category_detail = {i.split(':')[0]:dict() for i in imsi_list}
            # 카테고리 : []
            Category_frequence_dict = { x:0 for x in Category_dict }
            for word in top_word_list:
                for k,v_list in Category_dict.items():
                    if word in v_list:
                        Category_frequence_dict[k] += 1
                        if word in Category_detail[k]:
                            Category_detail[k][word] += 1
                        else:
                            Category_detail[k][word] = 1
            detail_val_list = []
            detail_index_list = []
            for k1,indict in Category_detail.items():
                for k2,val in indict.items():
                    detail_val_list.append(val)
                    detail_index_list.append(k2)

            detailFrame = pd.DataFrame(detail_val_list,index=detail_index_list)
            detailFrame.columns = ['개수']

            CategoryFrame = pd.DataFrame(Category_frequence_dict,index=[0])
            CategoryFrame = CategoryFrame.T
            CategoryFrame.columns = ['개수']
            CategoryFrame = CategoryFrame.loc[CategoryFrame['개수']>0]

            # 관심 카테고리 비중 그래프 그리기 ########################
            plt.figure()
            CategoryFrame['개수'].plot(kind='pie',autopct='%.2f%%')
            plt.title(f'{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_업데이트_{label}_관심카테고리')

            category_file_name = f'pie_graph_category_{label}.png'
            plt.savefig(category_file_name, dpi=600, bbox_inches='tight')

            print(CategoryFrame.index)

            # 키워드별 빈도 막대 그래프 :
            plt.figure()
            barFrame = pd.DataFrame(top_word_list,columns=['kwd'])
            barGroup = barFrame.groupby(by='kwd')['kwd']
            bardata = barGroup.count()


            bardata.plot(kind='barh')
            plt.title(f'{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_{label}_카테고리_세부내역')
            bar_file_name = f'bar_graph_category_{label}.png'
            plt.savefig(bar_file_name, dpi=600, bbox_inches='tight')
            # plt.show()

            fig, ax = plt.subplots()

            size = 0.3
            vals = np.array([[60., 32.], [37., 40.], [29., 10.]])

            cmap = plt.get_cmap("tab20c")
            outer_colors = cmap(np.arange(3) * 4)
            inner_colors = cmap(np.array([1, 2, 5, 6, 9, 10]))

            ax.pie(CategoryFrame['개수'],labeldistance=1.1, labels=CategoryFrame.index,radius=1, colors=outer_colors,
                   wedgeprops=dict(width=size, edgecolor='w'))

            ax.pie(detailFrame['개수'],labeldistance=0.7,labels=detailFrame.index, radius=1 - size, colors=inner_colors,
                   wedgeprops=dict(width=size, edgecolor='w'))

            ax.set(aspect="equal", title='Pie plot with `ax.pie`')
            plt.show()

            # top_Series = pd.Series(top_10_list)
            # result = top_Series.value_counts()
            # top_dict = dict()
            # for x in result.items():
            #     top_dict[x[0]] = x[1]

            # 워드 클라우드에 사용할 top 10
            # top_10_list = []
            # for textid,row in scoreFrame.T.iterrows():
            #     sort_key = row.sort_values(ascending=False)[:10].index
            #     print(sort_key)
            #     top_10_list.extend(sort_key)
            #
            # top_Series = pd.Series(top_10_list)
            # result = top_Series.value_counts()
            # top_dict = dict()
            # for x in result.items():
            #     top_dict[x[0]] = x[1]

            ########## 워드 클라우드###########
            # plt.figure()
            # mask = np.array(Image.open(image_path[label]))
            #
            # image_color = ImageColorGenerator(mask)
            #
            # wc = WordCloud(font_path='malgun.ttf', max_words=100, mask=mask,
            #                background_color='rgba(255,255,255,0)', mode='RGBA', random_state=43)
            # wc.generate_from_frequencies(top_dict)
            # newwc = wc.recolor(color_func=image_color)
            # plt.imshow(wc)
            # plt.title(f'update_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일')
            # plt.axis('off')
            #
            # # 워드클라우드 이미지로 저장하기
            # wcimgfilename = f'keyword_wordcloud/wcd_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_{label}.png'
            # plt.savefig(wcimgfilename, dpi=600, bbox_inches='tight')
            # print(wcimgfilename + '파일이 저장되었습니다.')
            # plt.close()
            ##########
        # end 감정별 데이터 분석

    # 각 업데이트별 데이터 분석


# 업데이트 하나만 가지고 테스트 해본다.
print(forFrame.iloc[[0],:])
analyData(forFrame.iloc[[1],:])