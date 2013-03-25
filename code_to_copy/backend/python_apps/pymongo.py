#!/usr/bin/env python
#-*- coding:utf8 -*-

import pymongo
conn = pymongo.Connection(host='127.0.0.1',port=27017)

db = conn.XXX_DATABASE
collection = db.XXX_collection
collection.insert(XXX)
for item in collection.find():
    XXX
conn.XXX_DATABASE.XXX_COLLECTION.remove() # 不加参数删除所有

collection.update({"XXX" : "XXX"}, {"$set" : {"XXX": "XXX"}}, upsert = False, safe = False, multi = False)
