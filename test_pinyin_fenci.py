#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 18:23
# Filename: test_pinyin_fenci.py
# Description: 
from pinyin_trie import PinyinTokenizer, Trie, TrieNode

tokenizer = PinyinTokenizer()
print tokenizer.tokenize('woaibeijingtiananmentiananmenshangtaiyangsheng')
print tokenizer.tokenize('zhida')
