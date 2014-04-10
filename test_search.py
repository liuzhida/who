#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 17:40
# Filename: test_search.py
# Description: 
from mmseg import seg_txt
from config import c

def search():

    word = "刘志达"
    key = list()
    data = list()

    #print len(word)
    #if len(word) <= 3:
    #    print "<=9"
    #    word = word.decode("utf-8")
    #    for n in word:
    #        print n,[n]
    #        if c.exists("index:" + n):
    #            key.append("index:" + n)
    #        #if c.exists("index:" + n.encode("utf-8")):
    #        #    key.append("index:" + n.encode("utf-8"))
    #else:
    #    for n in seg_txt(word):
    #        print n,[n]
    #        if c.exists("index:" + n):
    #            key.append("index:" + n)

    for n in seg_txt(word):
        if c.exists("index:" + n):
            key.append("index:" + n)

    if len(key) == 1:
        ids = c.smembers(key[0])
    else:
        ids = c.sinter(key)

    
    
    for id in ids:
        print id
        result = dict()
        result = c.hgetall(id)
        result['type'] = id.split(":")[0]
        data.append(result)
    for d in data:
        print d['name']


if __name__ == "__main__":
    search()
