import jieba
import numpy as np
import pandas as pd
import PIL.Image as Image
from wordcloud import WordCloud
from pyecharts import options as opts
from pyecharts.charts import Bar

from pyecharts.globals import ThemeType


def get_contents(path):
    df = pd.read_csv(path)
    comments = ''
    for i in df['评论内容']:
        comments += '，' + i.strip()
    return comments


def get_stopwords(paths):
    stopwords = []
    for path in paths:
        with open(path, mode='r', encoding='utf-8') as f:
            for word in f.readlines():
                if word not in stopwords:
                    stopwords.append(word.strip())
    stopwords.append(' ')
    return stopwords


def get_split_words(contents, stopwords):
    split_words = []
    for word in jieba.cut(contents):
        if word not in stopwords and len(word) > 1:
            split_words.append(word)
    return split_words


def get_top_words(words, num):
    tf_dic = {}
    for w in words:
        tf_dic[w] = tf_dic.get(w, 0) + 1
    return sorted(tf_dic.items(), key=lambda x: x[1], reverse=True)[:num]


if __name__ == '__main__':
    jieba.load_userdict('../words/my_dic.txt')

    stopwords_paths = [
        '../words/cn_stopwords.txt',
        '../words/baidu_stopwords.txt',
        '../words/hit_stopwords.txt',
        '../words/scu_stopwords.txt',
        '../words/my_stopwords.txt'
    ]
    comments_path = '../douban_comments.csv'

    contents = get_contents(comments_path)
    stopwords = get_stopwords(stopwords_paths)
    split_words = get_split_words(contents, stopwords)

    pic = np.array(Image.open('../file/pic.png'))
    wc = WordCloud(font_path='../file/方正粗黑宋简体.ttf', mask=pic, background_color='white', max_font_size=300,
                   min_font_size=5)
    wc.generate(' '.join(split_words))
    wc.to_file('../db_wordcloud.png')

    top_words = get_top_words(split_words, 30)
    word_list = []
    word_values = []
    for i in top_words:
        word_list.append(i[0])
        word_values.append(i[1])

    c = (
        Bar({"theme": ThemeType.MACARONS, "height": "1000px"})
            .add_xaxis(list(reversed(word_list)))
            .add_yaxis("词数", list(reversed(word_values)))
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts={"text": "《长津湖》豆瓣影评词频"})
            .render("../《长津湖》豆瓣影评词频.html")
    )
