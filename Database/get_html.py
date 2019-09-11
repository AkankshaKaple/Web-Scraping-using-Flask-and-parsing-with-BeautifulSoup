import requests
from pymongo import MongoClient
# from flask import Flask, request
import requests
import json

# app = Flask(__name__)
client = MongoClient()
db = client.store_HTMLs

# HTMLs = ['funding.html', 'jobs.html', 'linkedin.html', 'main.html',
#          'people.html', 'crunch_base.html']
data1 = {'1': 'a', '2': 'b'}
data2 = {'1': 'c', '2': 'd', '3': 'ddd', '4': 'sss'}
data3 = {'1': 'e', '2': 'f'}
data4 = {'1': 'sssss', '2': '', '3': 'ddd', '4': 'sss'}

db.My_Data1.insert(data1)
db.My_Data1.insert(data3)
db.My_Data4.insert(data2)
db.My_Data3.insert(data4)

# cursor = db.My_Data1.find({'1': 'e'})
# for i in cursor:
#     id = i['_id']

# cursor = db.My_Data2.find()
# for record in cursor:
#     print("Updated record : ", record)

# cursor = db.My_Data2.find()
# my_query = {'1': 'sssss'}
# new_values = {"$set": {"2": "Canyon 123"}}
#
# db.My_Data2.update_one(my_query, new_values)

# cursor = db.My_Data2.find()
# for record in cursor:
#     print("Updated record : ", record)

# d = dict((db, [collection for collection in client[db].collection_names()])
#          for db in client.database_names())
# print(d)

# database_name = 'MY_DATABASE_NAME'
# database = db[database_name]
collection = db.collection_names(include_system_collections=False)
flag = False
for collect in collection:
    if 'My_Data' == collect:
        flag = True
        break

# flag = [True for collect in collection if 'My_Data' in collect]
if flag:
    print("if  ",flag)
else:
    print('else :', flag)
