from string import ascii_letters
from nltk.tokenize import sent_tokenize
from wordcloud import WordCloud
from PIL import Image
from wordcloud import ImageColorGenerator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from gensim.models import word2vec
import matplotlib.pyplot as plt
from konlpy.tag import Okt
import nltk
plt.rc('font', family='Malgun Gothic')


image_path = {'긍정':'positive.png','부정':'negative.jpg','복합':'middle.png'}

filename = 'update_word_csv_v04.csv'
forFrame = pd.read_csv(filename,index_col=0,usecols=['update_id','year','month','day'])
# print(forFrame)
forFrame['fd'] = forFrame['year'].apply(lambda x : str(x))
forFrame['fd'] += forFrame['month'].apply(lambda x : '-'+str(x))
forFrame['fd'] += forFrame['day'].apply(lambda x : '-'+str(x))
# print(forFrame['fd'])
seri_list = []
percent_list = []
# 업데이트별 반응



def work(forFrame):

    nnnnnn = 1
    for itrow in forFrame.iterrows():

        okt = Okt()
        f_dict = {}
        plt.figure()
        frame = pd.read_csv(f'update_review_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일.csv',index_col=0)
        f_dict['긍정'] = frame[frame['LABEL']=='긍정']
        f_dict['부정'] = frame[frame['LABEL'] == '부정']
        f_dict['복합'] = frame[frame['LABEL'] == '복합']


        frame_stack = []
        for label,f in f_dict.items():
            print(label)

            frame_row = []  # 명 : 키워드 , 형: 키워드 , 동 : 키워드

            noun_s = set()  # score에 사용할추출 noun 데이터
            adjec_s = set()
            verb_s = set()
            unk_s = set()
            freq_dict = {}
            all_sentense_list = []
            item_cnt = 100
            for text in f['CONTENTS'][:item_cnt]:
                sent_l = sent_tokenize(text)
                # print('sent_l',len(sent_l))

                for sent in sent_l:
                    tokens = []  # word2vec 학습 데이터
                    pos = okt.pos(sent,norm=True)
                    # print(pos)
                    pos = [x for x in pos if x[0] not in('롤러','지금','다른') and len(x[0])>1]
                    tokens.extend([ x[0] for x in pos ])
                    noun_s.update([ x[0] for x in pos if x[1] in ['Noun'] ])
                    adjec_s.update([ x[0] for x in pos if x[1] in ['Adjective']])
                    verb_s.update([ x[0] for x in pos if x[1] in ['Verb'] ])
                    unk_s.update([ x[0] for x in pos if x[1] in ['Unknown'] ])

                    # 하나의 문장을
                    # print(tokens)
                    all_sentense_list.append(tokens)




            print(len(tokens))
            print(len(noun_s))
            print(len(adjec_s))
            print(len(verb_s))
            print(len(unk_s))
            # print(noun_s)
            with open(f'pumsa_list_{label}.txt','w',encoding='utf-8') as file:
                file.write('/'.join(noun_s))

            model = word2vec.Word2Vec(all_sentense_list,size=100,window=3,iter=30,hs=1,sg=1)
            # print(len(model.wv.vocab))
            topn = len(model.wv.vocab)
            noun_vocab = [x for x in model.wv.vocab.keys() if x in noun_s]
            adjec_vocab = [x for x in model.wv.vocab.keys() if x in adjec_s]
            verb_vocab = [x for x in model.wv.vocab.keys() if x in verb_s]
            pumsa_list = [('명사',noun_vocab),('형용사',adjec_vocab),('동사',verb_vocab)]
            # print(len(noun_vocab))
            # print(len(noun_s))
            # Wv = model.wv
            # vocab = model.wv.vocab
            model.save(f'model_{label}_{item_cnt}.model')

            for pumsa,pumsa_vocab in pumsa_list:

                # 유사도 행렬
                # sim matrix concat_data
                simi_matrix_list = []
                for noun in pumsa_vocab:
                    # 절대값?
                    sim_dict = { x[0]:x[1] for x in model.wv.most_similar(positive=[noun],topn=topn) if x[0] in pumsa_vocab }
                    sim_dict[noun] = 1

                    simi_matrix_list.append(sim_dict)
                print('simi_matrix_list',len(simi_matrix_list))
                # sim Frame
                simFrame = pd.DataFrame(simi_matrix_list,index=pumsa_vocab)
                # print(simFrame)
                print(simFrame.shape)
                tf_list = []
                for sent in all_sentense_list:
                    # print(sent)
                    tf_dict = { n:0 for n in pumsa_vocab}
                    for s in sent:
                        if s in pumsa_vocab:
                            tf_dict[s] += 1
                    tf_list.append(tf_dict)

                tfFrame = pd.DataFrame(tf_list).T

                nFame = pd.DataFrame(np.dot(simFrame,tfFrame),index=pumsa_vocab).T
                # 프레임 출력
                # print(nFame)

                top_dict = {}
                # 문장의 대표 키워드 10위씩 뽑아내서
                # 키워드 빈도수 사전에 집어넣기
                for row in nFame.iterrows():
                    # 한행 출력
                    # print(row)
                    rows = row[1].sort_values(ascending=False)[:10].index
                    for r in rows:
                        if r in top_dict:
                            top_dict[r] += 1
                        else:
                            top_dict[r] = 1
                # print(len(top_dict))
                ########## 워드 클라우드 ##############
                if pumsa == '명사':
                    plt.figure()
                    mask = np.array(Image.open(image_path[label]))

                    image_color = ImageColorGenerator(mask)

                    wc = WordCloud(font_path='malgun.ttf',max_words=100,mask=mask,
                                    background_color='rgba(255,255,255,0)',mode='RGBA', random_state=43)
                    wc.generate_from_frequencies(top_dict)
                    newwc = wc.recolor(color_func=image_color)
                    plt.imshow(wc)
                    plt.title(f'update_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일')
                    plt.axis('off')

                    # 워드클라우드 이미지로 저장하기
                    wcimgfilename = f'keyword_wordcloud/wcd_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_{label}_{pumsa}.png'
                    plt.savefig(wcimgfilename, dpi=600, bbox_inches='tight')
                    print(filename + '파일이 저장되었습니다.')
                    plt.close()
                    ############################################

                top_dict = sorted(top_dict,key=lambda x:top_dict[x],reverse=False)

                # print(type(top_dict))
                print(label,'(topic keyword) :',top_dict[:10])
                # ex 품사 : 명사 , 긍정 :
                frame_row.append('/'.join(top_dict))
                # end 키워드 subset
            #end pumsa별 키워드
            frame_stack.append(frame_row)
        # end 긍부복:
        save_frame = pd.DataFrame(frame_stack,index=['긍정','부정','복합'],columns=['명사','형용사','동사'])
        save_frame.to_csv(f'keyword02/keyword_{itrow[1][0]}년{itrow[1][1]}월{itrow[1][2]}일_02.csv')
        # ################## 워드 클라우드
        # ko = nltk.Text(tokens=tokens)
        # concat_data = ko.vocab().most_common(500)
        # tmp_dict = dict(concat_data)
        # wc = WordCloud(font_path='malgun.ttf',
        #                 background_color='white', random_state=43)
        # wc.generate_from_frequencies(tmp_dict)
        # plt.imshow(wc)
        # plt.title(f'update_{row[1][-1]}')
        # plt.axis(False)
        # filename = f'update_{row[1][-1]}.png'
        # plt.savefig(filename, dpi=400, bbox_inches='tight')
        # ############### 워드 클라우드
        if nnnnnn == 3:
            break
        nnnnnn +=1

# plt.show()

work(forFrame)