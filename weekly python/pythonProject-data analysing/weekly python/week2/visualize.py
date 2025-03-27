import pandas as pd
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt

# 读取 CSV 文件
csv_file = 'douban_top250_extended.csv'
df = pd.read_csv(csv_file)

# 合并所有电影简介
all_quotes = ' '.join(df['简介'])

# 使用 jieba 进行中文分词
words = jieba.lcut(all_quotes)
text = ' '.join(words)

# 生成词云图
wordcloud = WordCloud(font_path='simhei.ttf', background_color='white').generate(text)

# 显示词云图
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
