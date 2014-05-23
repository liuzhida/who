#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-05-09 15:31
# Filename: add_index.py
# Description: 
from mmseg import seg_txt
from config import c

def add(word, id):
    for n in seg_txt(word):
        c.sadd("index:" + n, "person:"+id)


if __name__ == "__main__":
    add("redis","zhida")
    add("lua","zhida")
