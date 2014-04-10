#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-09 17:02
# Filename: build_index.py
# Description: 
from config import c
from pypinyin import lazy_pinyin
from mmseg import seg_txt


def person_index():
    for key in c.keys("person:*"):
        data = c.hgetall(key)

        #name

        c.sadd("index:" + key.split(":")[-1], key)
        name = data['name']
        for n in seg_txt(name):
            c.sadd("index:" + n, key)
        name = name.decode("utf-8")
        if ord(name[0]) <= 127:
            name = name.split()
            for n in name:
                print n,
                n = n.lower()
                c.sadd("index:" + n, key)
        else:
            for n in name:
                print n,
                c.sadd("index:" + n, key)
        for i in lazy_pinyin(name):
            print i,
            c.sadd("index:" + i, key)

        #school

        word = data['school']
        if word:
            for i in seg_txt(word):
                print i,
                c.sadd("index:" + i, key)

        #xingzuo
        word = data['xingzuo']
        if word:
            for i in seg_txt(word):
                print i,
                c.sadd("index:" + i, key)

        #hometown
        word = data['hometown']
        if word:
            for i in seg_txt(word):
                print i,
                c.sadd("index:" + i, key)

        #sex
        word = data['sex']
        if word:
            for i in seg_txt(word):
                pass
                c.sadd("index:" + i, key)

        print 

def pa_index():
    for key in c.keys("area:*"):
        data = c.hgetall(key)
        name = data['name']

        if "&" in name:
            name = name.split("&")
        else:
            name = name.split()

        for n in name:
            n = n.lower()
            n = n.strip()
            print n, "|",
            c.sadd("index:" + n, key)
        print


def product_index():
    for key in c.keys("product:*"):
        data = c.hgetall(key)
        name = data['name']

        if "/" in name:
            name = name.split("/")
        else:
            name = name.split()

        for n in name:
            n = n.lower()
            n = n.strip()
            print n, "|",
            c.sadd("index:" + n, key)
        print


if __name__ == "__main__":
    #for key in c.keys("index:*"):
    #    c.delete(key)
    person_index()
    pa_index() 
    product_index()
