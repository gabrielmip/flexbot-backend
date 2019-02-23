from collections import namedtuple
import json

def dict_to_object(d):
    return namedtuple('X', d.keys())(*d.values())
