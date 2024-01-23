#!/usr/bin/env python3
"""
    provides some stats about Nginx logs stored in MongoDB
"""
import  pymongo
from pymongo import MongoClient


client = MongoClient('mongodb://127.0.0.1:27017')
collection = client.logs.nginx
x = collection.count_documents({})
print(f"{x} logs")
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
print("Methods:")
for method in methods:
    rst = collection.count_documents({'method': method})
    print(f'\tmethod {method}: {rst}')
st = collection.count_documents({'path': '/status', 'method': "GET"})
print(f'{st} status check')
