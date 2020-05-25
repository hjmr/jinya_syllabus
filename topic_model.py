from gensim import corpora, models, similarities
import gensim
import math
import csv

from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
from collections import defaultdict

import pandas as pd
import itertools


df = pd.read_csv('syllabus_2018.csv', usecols=[0])
class_names = df.values.tolist()
class_names  = list(itertools.chain.from_iterable(class_names))

f = open("theme_words_2018.csv", "r")
reader = csv.reader(f)
texts = [ e for e in reader ]
f.close()

# トピック数の設定
NUM_TOPICS = 8

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
lda_model = LdaModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=dictionary)




# テストデータをモデルに掛ける
score_by_topic = defaultdict(int)
test_corpus = [dictionary.doc2bow(text) for text in texts]

# クラスタリング結果を出力
for unseen_doc, raw_train_text in zip(test_corpus, class_names):
    print(raw_train_text, end='\t')
    for topic, score in lda_model[unseen_doc]:
        score_by_topic[int(topic)] = float(score)
    for i in range(NUM_TOPICS):
        print('{:.2f}'.format(score_by_topic[i]), end='\t')
    print()


# Visualize

from wordcloud import WordCloud
from PIL import Image
import matplotlib
import matplotlib.pylab as plt
import numpy as np
from tqdm import tqdm
import math

np.random.seed(0)
FONT = "/Library/Fonts/Arial Unicode.ttf"


ncols = math.ceil(NUM_TOPICS/2)
nrows = math.ceil(lda_model.num_topics/ncols)
fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(15,7))
axs = axs.flatten()

def color_func(word, font_size, position, orientation, random_state, font_path):
    return 'darkturquoise'

for i, t in enumerate(range(lda_model.num_topics)):

    x = dict(lda_model.show_topic(t, 30))
    im = WordCloud(
        font_path=FONT,
        background_color='white',
        color_func=color_func,
        random_state=0
    ).generate_from_frequencies(x)
    axs[i].imshow(im)
    axs[i].axis('off')
    axs[i].set_title('Topic '+str(t))

plt.tight_layout()
plt.savefig("./visualize.png")
