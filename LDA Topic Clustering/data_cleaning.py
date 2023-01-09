# -*- coding:utf-8 -*-
import jieba

"""
Perform word segmentation and filter stop words
"""

def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords_sum.txt',
                                               encoding='UTF-8').readlines()]
    return stopwords



def seg_depart(sentence):
    sentence_depart = jieba.cut(sentence.strip())
    stopwords = stopwordslist()
    outstr = ''
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr



filename = "长津湖正向.txt"
outfilename = "长津湖正向分词后.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')

for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')
    print("-------------------正在分词和去停用词-----------")
outputs.close()
inputs.close()
print("删除停用词和分词成功!!!")
