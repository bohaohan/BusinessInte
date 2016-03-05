# -*- coding: UTF-8 -*-
import codecs

__author__ = 'bohaohan'
import json,simplejson
from datetime import date, datetime

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

f = open('tsxbb_j.json')
# string = f.readline()
# string = json.loads(string, strict=False)
# print string
# c = json.load(string)
# print c
a = 0
file = f.read()
file += "*123*"
strings = file.split("*123*")
print len(strings)
for string in strings:
    if not string:
        break
    string = string.replace("'", "‘").replace("\\","\\\\")
    a += 1
    print a
    try:
        #try:
        string = json.loads(string, strict=False)
        #print string['title'] + '\n'
        keys = string.keys()
        for key in keys:
            print key
        # break
    except:
        print string
    # except:
    #     print string
