#! python

import requests
import json,config
from urllib import quote_plus
import hashlib

def send_comment(uid,cmt):
    host = config.host_url
    cmt['secret'] = config.comment_secret
    r = requests.post(host+quote_plus(uid),json=cmt)
    return r.json()

def sign(s):
    md5 = hashlib.md5((s+'|233|'+config.server_secret).encode('utf-8')).hexdigest()
    return md5

