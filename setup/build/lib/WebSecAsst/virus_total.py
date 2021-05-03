#! /home/chs/anaconda3/envs/sw/bin/python 
import requests
import json
import sys 
import hashlib
from os import path
import time

url = 'https://www.virustotal.com/vtapi/v2/file/report'
localpath = sys.argv[1]
if path.exists(localpath):
    with open(localpath, "rb") as f:
        file_hash = hashlib.md5()
        chunk = f.read(8192)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(8192)

    md5hash=file_hash.hexdigest()

    params = {'apikey': 'abbdcbd4548c2338e7c7177f6ee5e58762ba1d0af1fbd6336c65baff165c2f42', 'resource': md5hash }

    response = requests.get(url, params=params)
    response=response.json()
    if response['response_code']==1 and response['positives']>0:
        print("\tMalicious")
    else:
        print("\tSafe")
else:
    print("File Deleted/Moved to other location")