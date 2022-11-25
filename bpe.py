#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 14:01:51 2022

@author: ahenschel

Byte-pair Encoding

Example From Jurafsky/Martin, Fig 2.13
"""

from collections import Counter
def extractVocabulary(corpus):
    return list(set(''.join(corpus.keys())))

def mostFreqPair(corpus):
    c2grams = Counter()
    for word, count in corpus.items():
        word_ = word.split()
        twograms = [tuple(word_[i:i+2]) for i in range(len(word_)-1)]
        c2grams += Counter(twograms*count)
    return c2grams.most_common()[0][0]

def updateCorpus(corpus, doubleToken):
    dt1 = ' '.join(doubleToken)
    dt2 = ''.join(doubleToken)
    return {word.replace(dt1, dt2):count for word, count in corpus.items()}
    
def bpe(corpus, k):
    V = extractVocabulary(corpus)
    for i in range(k):    
        tnew = mostFreqPair(corpus)
        V.append(''.join(tnew))
        corpus = updateCorpus(corpus, tnew)
    return V, corpus

def tokenParser(word, tokens):
    for token in tokens:
        token2 = ''.token
        word.replace

k = 15 # so to match the book
corpus = {'l o w _': 5, 
          'l o w e s t _': 2,
          'n e w e r _': 6,
          'w i d e r _': 3,
          'n e w _': 2}

V, corpus = bpe(corpus, k)

    


