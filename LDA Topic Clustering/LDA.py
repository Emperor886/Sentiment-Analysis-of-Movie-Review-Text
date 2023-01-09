# -*- coding:utf-8 -*-
import numpy as np
from gensim import corpora, models
import os
import sys
sys.stderr = open(os.devnull, "w")  # silence stderr
import gensim.corpora as corpora
sys.stderr = sys.__stderr__  # unsilence stderr


"""
Topic clustering based on LDA model
"""

if __name__ == '__main__':
    f = open('长津湖正向分词后.txt', encoding='utf-8') 
    texts = [[word for word in line.split()] for line in f]
    f.close()
    M = len(texts)
    print('文本数目:%d 个' % M)

    dictionary = corpora.Dictionary(texts)
    V = len(dictionary)
    print('词的个数:%d 个' % V)
    corpus = [dictionary.doc2bow(text) for text in texts] 

    corpus_tfidf = models.TfidfModel(corpus)[corpus]

    num_topics = 10 
    lda = models.LdaModel(corpus_tfidf, num_topics=num_topics,
                          id2word=dictionary,
                          minimum_probability=0.001,
                          alpha=0.01, eta=0.01,
                          update_every=1, chunksize=100, passes=1)
    doc_topic = [a for a in lda[corpus_tfidf]]
    print('Document-Topic:')
    print(doc_topic)

    
    num_show_topic = 5  
    print('文档的主题分布:')
    doc_topics = lda.get_document_topics(corpus_tfidf)  
    idx = np.arange(M) 
    for i in idx:
        topic = np.array(doc_topics[i])
        topic_distribute = np.array(topic[:, 1])
        topic_idx = topic_distribute.argsort()[:-num_show_topic - 1:-1]
        print('第%d 个文档的前%d 个主题:' % (i, num_show_topic))
        print(topic_idx)
        print(topic_distribute[topic_idx])


    num_show_term = 10  
    for topic_id in range(num_topics):
        print('主题#%d:\t' % topic_id)
        term_distribute_all = lda.get_topic_terms(topicid=topic_id)  
        term_distribute = term_distribute_all[:num_show_term] 
        term_distribute = np.array(term_distribute)
        term_id = term_distribute[:, 0].astype(np.int)
        print('词:', end="")
        for t in term_id:
            print(dictionary.id2token[t], end=' ')#.encode('GBK', 'ignore').decode('GBK')
            print('概率:', end="")
            print(term_distribute[:, 1])


    with open('topicword.txt', 'w', encoding='utf-8') as tw:
        for topic_id in range(num_topics):
            term_distribute_all = lda.get_topic_terms(topicid=topic_id, topn=20)
            term_distribute = np.array(term_distribute_all)
            term_id = term_distribute[:, 0].astype(np.int)
            for t in term_id:
                tw.write(dictionary.id2token[t] + " ")
            tw.write("\n")
