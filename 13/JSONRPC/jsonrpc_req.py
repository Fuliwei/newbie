#!/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import json
import requests

headers = {'content-type': 'application/json'}
url = "http://127.0.0.1:888/api"
data = { 
    'jsonrpc':'2.0',
#   'method': 'App.index',    #�������޲�����method
#   'method': 'App.name',     #������ָ��������method
#   'method': 'App.user',      #�����˲���������method��ͨ���βλ�ȡ����
    'method': 'App.users',     #�����˲���������method,get_json��ȡ����
    'id':'4',
    'params':{
        'name':'wd',   #�޲�����method���˴�Ϊ�գ�ָ��������method��ֻ�ܱ���һ������
        'age':'18'
    }   

}

r = requests.post(url, headers=headers,json=data)

print r.status_code
#print r.text
re = json.loads(r.text)
print re
print type(re)
print re["result"]

