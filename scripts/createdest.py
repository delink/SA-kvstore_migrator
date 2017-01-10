#!/usr/bin/env python3

from splunkkvstore import splunkkvstore

dest_splunk = splunkkvstore("https://172.21.42.103:8089","admin","temp1234")
dest_splunk.login()

coll_list = dest_splunk.get_collection_list("nobody","testkvstore")
for coll in coll_list:
	if coll_list[coll]['sharing'] == 'app':
		print("Collection {}:".format(coll))
		print("Creating existing collection")
		results = dest_splunk.create_collection("nobody","testkvstore",coll)
