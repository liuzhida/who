#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-10 18:51
# Filename: img.py
# Description: 
import glob
import os
from config import c

def rename():
    for file in glob.glob("static/pic/*"):
        print file
        name = file.split("_")[0]
        jpg = file.split(".")[-1]
        new = name + "." + jpg
        print new
    
        os.rename(file,new)

def into():
    for file in glob.glob("static/img/*"):
        pic = file.split("/")[-1]
        name = pic.split(".")[0]
        print name
        if c.exists("person:"+name):
            c.hset("person:" + name, "img", "http://who.wandoulabs.com/static/img/"+pic)

 
if __name__ == "__main__":
    into()
