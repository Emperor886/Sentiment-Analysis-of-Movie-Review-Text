# -*- coding:utf-8 -*-
from collections import defaultdict
import os
import re
import jieba
import codecs
import pandas as pd
from numpy import *

"""
Build a sentiment dictionary and calculate the sentiment value of film review text
"""

jieba.setLogLevel(jieba.logging.INFO)

stopwords = set()
fr = open('./stopwords_sum.txt', 'r', encoding='utf-8')
for word in fr:
    stopwords.add(word.strip())
not_word_file = open('./否定词.txt', 'r+', encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]
degree_file = open('./程度副词.txt', 'r+', encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
with open('./stopwords_new.txt', 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_list):
            f.write(word + '\n')


def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    stopwords = set()
    with open('./stopwords_new.txt', 'r', encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    return list(filter(lambda x: x not in stopwords, seg_result))


def classify_words(word_list):
    sen_file = open('./情感词.txt', 'r+', encoding='utf-8')
    sen_list = sen_file.readlines()
    sen_dict = defaultdict()
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]

    not_word_file = open('./否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.read().splitlines()
    degree_file = open('./程度副词.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]
    sen_word = dict()
    not_word = dict()
    degree_word = dict()
    for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys():
            #and word not in not_word_list and word not in degree_dict.keys():
            sen_word[i] = sen_dict[word]
        elif word in not_word_list: #and word not in degree_dict.keys():
            not_word[i] = -1
        elif word in degree_dict.keys():
            degree_word[i] = degree_dict[word]
    sen_file.close()
    not_word_file.close()
    degree_file.close()
    return sen_word, not_word, degree_word


def score_sentiment(sen_word, not_word, degree_word, seg_result):
    W = 1
    score = 0
    sentiment_index = -1
    sentiment_index_list = list(sen_word.keys())
    for i in range(0, len(seg_result)):
        if i in sen_word.keys():
            # W = int(float(sen_word[i]))
            score += W * float(sen_word[i])
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                for j in range(sentiment_index_list[sentiment_index],sentiment_index_list[sentiment_index + 1]):
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])

        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


def sentiment_score(sentence):
    seg_list = seg_word(sentence)
    sen_word, not_word, degree_word = classify_words(seg_list)
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score


def data_load():
    df_comment = pd.read_excel('./水门桥.xlsx')
    df_comment = df_comment.iloc[:, 4:5]
    df_comment.columns = ['评论内容']
    print(len(df_comment))
    score_list = []
    print(df_comment)
    for index, i in df_comment.itertuples():
        word_score = sentiment_score(i)
        score_list.append(word_score)
    mean = sum(score_list) / len(score_list)
    print("水门桥情感平均分为:", mean)
    return mean


if __name__ == "__main__":
    mean = data_load()
    print('不喜欢这个题材', sentiment_score('不喜欢这个题材'))
    print("人民英雄永垂不朽！", sentiment_score('人民英雄永垂不朽！'))
    # print('特别无聊', sentiment_score('特别无聊'))
