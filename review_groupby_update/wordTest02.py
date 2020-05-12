import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from wordcloud import STOPWORDS
from wordcloud import ImageColorGenerator
from PIL import Image
import pandas as pd
from pandas import DataFrame
from konlpy.tag import Okt

Tw = Okt()

plt.rc('font', family='Malgun Gothic')

image_file = 'google.png'
img_file = Image.open(image_file)

gp_mask = np.array(img_file)

mystopwords = open('hangle_stop_word.txt', encoding='UTF-*').readlines()  # 분석에 불필요한 불용어 처리 작업

# mystopwords.add('said')
# mystopwords.update(['',''])
#print(mystopwords)


# print(len(mystopwords))
fontpath = 'malgun.ttf'
WC = WordCloud(font_path=fontpath, background_color='white', max_words=2000, mask=gp_mask, stopwords=mystopwords)

stevefile = 'review_label_02.csv'
read_data = pd.read_csv(stevefile, encoding='UTF-8')
#print(type(read_data))

mycolumns = ['label','text']
read_data = DataFrame(read_data,  columns=mycolumns)
#print(type(read_data))

posit_data = read_data[read_data['label'] == '부정']
#rint(type(posit_data))


posit_list = []
for idx in range(0, len(posit_data)):
    ptext = posit_data.iloc[idx]['text'] + ' '
    ptext = Tw.pos(ptext)
    posit_list.append(ptext)

new_posit_list = []
for posit in posit_list:
    for word, tag in posit:
        if tag in ['Noun']:
            new_posit_list.append(word + ' ')

#print(new_posit_list)

posit_str = ','.join(new_posit_list)
WC = WC.generate(posit_str)
print(WC.words_)

##################################################
logo_file = 'google.png'
logo_mask = np.array(Image.open(logo_file))

image_color = ImageColorGenerator(logo_mask)
newx = WC.recolor(color_func=image_color, random_state=42)

plt.figure(figsize=(12, 12))
plt.imshow(WC, interpolation='bilinear')
plt.axis('off')

filename = 'wcd_posit_negative.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')

plt.show()

print('finished')





# likedata = read_data.loc[:]['label']
# print(likedata)
# words = WC.generate(read_data.loc['text'])
# print(words)


# WC = WC.generate(text)
# print(WC.words_)
#
# logo_file = 'google.png'
# logo_mask = np.array(Image.open(logo_file))
#
# image_color = ImageColorGenerator(logo_mask)
# newx = WC.recolor(color_func=image_color, random_state=42)
#
# plt.figure(figsize=(12, 12))
# plt.imshow(WC, interpolation='bilinear')
# plt.axis('off')
#
# filename = 'wordTest_02.png'
# plt.savefig(filename, dpi=400, bbox_inches='tight')
#
# plt.show()
#
# print('finished')