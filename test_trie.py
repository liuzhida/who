#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 15:04
# Filename: test_trie.py
# Description: 

import pickle
# 也可以这样：
# import cPickle as pickle

obj = {"a": 1, "b": 2, "c": 3}

# 将 obj 持久化保存到文件 tmp.txt 中
pickle.dump(obj, open("tmp.txt", "w"))

# do something else ...

# 从 tmp.txt 中读取并恢复 obj 对象
obj2 = pickle.load(open("tmp.txt", "r"))

print obj2
