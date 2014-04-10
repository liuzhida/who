#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 14:51
# Filename: test_pinyin.py
# Description: 

from pypinyin import lazy_pinyin, TONE2

def get_pinyin(string):
    test = pinyin.PinYin()
    test.load_word()
    print "out: %s" % str(test.hanzi2pinyin(string=string))


if __name__ == "__main__":
    with open("employee.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        name = data[1]
        print name,
        for i in lazy_pinyin(name.decode("utf-8")):
            print i,
        print
