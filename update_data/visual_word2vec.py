# 참고 https://stackoverflow.com/questions/43776572/visualise-word2vec-generated-from-gensim

from sklearn.manifold import TSNE
import matplotlib as mpl
import matplotlib.pyplot as plt
import gensim
import gensim.models as g
import pandas as pd

mpl.rcParams['axes.unicode_minus'] = False
plt.rc('font',family='Malgun Gothic')

model_name = 'update_model.model'
model = g.Doc2Vec.load(model_name)

vocab = list(model.wv.vocab)
X = model[vocab]

tsne = TSNE(n_components=2)

X_tsne = tsne.fit_transform(X[:,:])

df = pd.DataFrame(X_tsne,index=vocab[:],columns=['x','y'])
fig = plt.figure()
fig.set_size_inches(40, 20)
ax = fig.add_subplot(1, 1, 1)

ax.scatter(df['x'],df['y'])

for word,pos in df.iterrows():
    ax.annotate(word,pos)

plt.show()