import pandas as pd
from gensim.models import word2vec

for num in range(1,5):
    modelname = 'review_model_score{}.model'.format(num)
    model = word2vec.Word2Vec.load(modelname)

    print(len(model.wv.vocab)) # 15189
    print(model.wv.vector_size) # 200
    topn_len = len(model.wv.vocab)
    vocabs = model.wv.vocab
    keys = list(vocabs.keys())
    print(type(keys))

    column_dict = dict()
    for x in keys:
        column_dict[x] = list()
    index_list = list()

    for key in keys:
        row = model.wv.most_similar(positive=[key],topn=topn_len )
        for x,y in row:
            column_dict[x].append(y)
        column_dict[key].append(1)
    print('finish step1')
    similar_frame = pd.DataFrame(column_dict,index=keys)
    similar_frame.to_csv('review_similar_matrix_score{}.csv'.format(num))
    print('finish step2')