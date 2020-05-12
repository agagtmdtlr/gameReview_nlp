import pandas as pd

df = pd.read_csv('review_sentence_csv_v03.csv')

score_wordSet_list = []
# 각 스코어별 말 뭉치를 만든다.
for num in range(1,6):
    score_Seriese = df.loc[df['score']==num,'sentence']
    sentence_list = []
    word_Set = set()
    for sent in score_Seriese:
        imsi = sent.split(' ')
        word_Set.update(imsi)

    imsi_frame = pd.DataFrame(word_Set,columns=['word'])
    imsi_frame.to_csv('score_data/review_wordSet_score{}.csv'.format(num))
    print(len(imsi_frame))
    score_wordSet_list.append(word_Set)


for num in range(1,6):
    score_Seriese = df.loc[df['score']==num]
    print(type(score_Seriese))
    review_ids = score_Seriese['review_id'].unique()
    onehot_list = []
    for id in review_ids:
        onehotrow = {w: 0 for w in score_wordSet_list[num - 1]}
        seri = df.loc[df['review_id']==id,'sentence']
        for x in seri:
            l = x.split(' ')
            for i in l:
                onehotrow[i] += 1
        onehot_list.append([id,onehotrow])

    onehot_frame = pd.DataFrame(columns=score_wordSet_list[num-1])
    for one in onehot_list:
        imsi_frame = pd.DataFrame(one[1],index=[one[0]])
        onehot_frame = pd.concat([onehot_frame,imsi_frame])
    onehot_frame.to_csv('review_one_hot_encoding_score{}.csv'.format(num))
