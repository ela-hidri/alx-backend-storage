#!/usr/bin/env python3
"""
pymongo
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """
    changes all topics of a school document based on the name
    """
    mongo_collection.update_one({"name": name}, {"$set": {'topics': topics}})
