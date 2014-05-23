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

def add_function(data):
    name = data[3]
    id = c.get("fname:" + name)
    if not id:
        if "Operation" in name:
            c.sadd("member:ops", data[0])
        else:
            print name, data[0], "failed"
    else:
        c.sadd("member:"+id, data[0])


def init_intern():
    with open("intern_final.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        id = data[0]
        result['name'] = data[1]
        result['sex'] = data[2]
        result['function'] = data[3]
        result['ladder']    = data[4]
        result['PA'] = data[5]
        result['manager']   = data[6]
        result['phone']     = data[7]
        result['mail']      = data[8]
        result['edate']     = data[10]
        result['hometown']  = data[11]
        result['xingzuo']   = data[13]
        result['school']    = data[14]
        result['id'] = id

        add_function(data)

        manager = ""
        for key in c.keys("person:*"):
            name = c.hget(key, "name")
            if result['manager'] == name:
                manager = key.split(":")[-1]
                result['manager'] = manager
        if not manager:
            print id, result['manager'], "no manager"
        c.hmset("person:" + id, result)
        c.sadd("member:"+result['PA'], id)


def init_person():
    with open("full_time_final.csv") as f:
        lines = f.readlines()

    for line in lines:
        result = dict()
        data = line.split(",")
        id = data[0]
        result['name']      = data[1]
        result['sex']       = data[2]
        result['function']  = data[3]
        result['ladder']    = data[4]
        result['PA']        = data[5]
        result['manager']   = data[6]
        result['phone']     = data[7]
        result['mail']      = data[8]
        result['edate']     = data[10]
        result['hometown']  = data[11]
        result['xingzuo']   = data[13]
        result['school']    = data[16]
        result['objective'] = data[19]
        result['id'] = id

        add_function(data)

        manager = ""
        for key in c.keys("person:*"):
            name = c.hget(key, "name")
            if result['manager'] == name:
                manager = key.split(":")[-1]
                result['manager'] = manager
        if not manager:
            print id, result['manager'], "no manager"
        c.hmset("person:" + id, result)
        c.sadd("member:"+result['PA'], id)


def init_PA():

    for key in c.keys("area:*"):
        print c.delete(key)
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
        result['mail'] = data[4].strip()
        result['id'] = data[0]

        #id = data[4].strip("-team@wandoujia.com")
        c.hmset("area:" + name, result)
        for k, v in result.items():
            print k, v


def init_Function():
    with open("function.csv") as f:
        lines = f.readlines()

    #for key in c.keys('product:*'):
    #    c.delete(key)
    for line in lines:
        result = dict()
        data = line.split(",")
        name = data[0]
        result['name'] = data[0]
        print result['name']
        #result['pm'] = data[2]
        #result['tl'] = data[3]
        result['objective'] = data[2].lstrip("Objective：")
        #print result['objective']
        #result['pm'] = data[2]
        result['okr'] = data[3]
        result['mail'] = data[4]

        mail = data[4]
        id = mail.split("-")[0]
        #print id
        result['id'] = id
        c.hmset("function:" + id, result)
        c.set("fname:" + name, id)
        #c.sadd("productof:" + data[0], id)
        #for k, v in result.items():
        #    print k, v


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
        result['id'] = id
        c.hmset("product:" + id, result)
        c.sadd("productof:" + data[0], id)
 
def init_fix():
    #for key in c.keys("person:*"):
    #    print c.hget(key,"manager")
    for key in c.keys("fname:*"):
        print c.delete(key)
        

if __name__ == "__main__":
    #init_PA()
    #init_person()
    #init_intern()
    #init_Product()
    #init_fix()
    init_Function()
