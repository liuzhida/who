#!/usr/bin/env python
# -*-coding:utf-8-*-
#
# Author: liuzhida - zhida@wandoujia.com
# Blog: http://liuzhida.com
# Last modified: 2014-04-09 11:12
# Filename: init.py
# Description:
import json
import redis

from config import c

def init_intern():
    with open("intern.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        id = data[0]
        result['name'] = data[1]
        result['sex'] = data[2]
        result['function'] = data[3]
        result['PA'] = data[4]
        result['manager'] = data[5]
        result['phone'] = data[6]
        result['mail'] = data[7]
        result['edate'] = data[9]
        result['hometown'] = data[10]
        result['xingzuo'] = data[12]
        result['school'] = data[13]

        manager = ""
        for key in c.keys("person:*"):
            name = c.hget(key, "name")
            if result['manager'] == name:
                manager = key.strip("person:")
                result['manager'] = manager
        if not manager:
            print id
        c.hmset("person:" + id, result)
        c.sadd("member:"+result['PA'], id)


def init_person():
    with open("full-time.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        id = data[0]
        result['name']      = data[1]
        result['sex']       = data[2]
        result['function']  = data[3]
        result['PA']        = data[4]
        result['manager']   = data[5]
        result['phone']     = data[6]
        result['mail']      = data[7]
        result['edate']     = data[9]
        result['hometown']  = data[10]
        result['xingzuo']   = data[12]
        result['school']    = data[15]

        manager = ""
        for key in c.keys("person:*"):
            name = c.hget(key, "name")
            if result['manager'] == name:
                manager = key.strip("person:")
                result['manager'] = manager
        if not manager:
            print id
        c.hmset("person:" + id, result)
        c.sadd("member:"+result['PA'], id)


def init_PA():
    with open("PA.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        name = data[0]
        result['name'] = data[0]
        result['owner'] = data[1]
        result['objective'] = data[2]
        result['okr'] = data[3]
        result['mail'] = data[4]
        #id = data[4].strip("-team@wandoujia.com")
        c.hmset("area:" + name, result)
        for k, v in result.items():
            print k, v


def init_Product():
    with open("Product.csv") as f:
        lines = f.readlines()

    #for key in c.keys('product:*'):
    #    c.delete(key)
    for line in lines:
        result = dict()
        data = line.split(",")
        name = data[1]
        result['PA'] = data[0]
        result['name'] = data[1]
        result['pm'] = data[2]
        result['tl'] = data[3]
        result['objective'] = data[5]
        result['okr'] = data[6]
        result['mail'] = data[7]
        mail = data[7]
        id = mail.split("-")[0]
        print id
        c.hmset("product:" + id, result)
        #for k, v in result.items():
        #    print k, v


if __name__ == "__main__":
    #init_person()
    init_intern()
    #init_PA()
    #init_Product()
