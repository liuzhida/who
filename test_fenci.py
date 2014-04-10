#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 13:38
# Filename: test_fenci.py
# Description: 
from mmseg import seg_txt

#word = word.encode("utf-8")
word = "liuzhida"

words = []
indexs = []
for i in seg_txt(word):
    print i

from pypinyin import pinyin, lazy_pinyin

print lazy_pinyin(u'刘志达')
print lazy_pinyin(u'liuzhida')
