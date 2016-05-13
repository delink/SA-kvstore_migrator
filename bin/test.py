#!/usr/bin/env python3

import requests
import json
requests.packages.urllib3.disable_warnings()

src_url = "https://172.21.42.102:8089"
dest_url = "https://172.21.42.103:8089"

def login(url,username,password):
	creds_payload = { 'cookie': '1', 'username': username, 'password': password }
	s = requests.Session()
	r = s.post(url+"/services/auth/login", creds_payload, verify=False)
	r.raise_for_status()
	return s

r = s.get(src_url+"/servicesNS/-/testkvstore/storage/collections/config?output_mode=json")
r.raise_for_status()
srcspl_coll_list = r.json()
r.raise_for_status() 

for entry in srcspl_coll_list['entry']:
	print(entry['id'])
