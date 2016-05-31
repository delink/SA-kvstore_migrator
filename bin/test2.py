#!/usr/bin/env python3

# Second attempt at test.py, now with the new library

from splunkkvstore import splunkkvstore

src_splunk = splunkkvstore("https://172.21.42.102:8089","admin","temp124")
src_splunk.login()

dest_splunk = splunkkvstore("https://172.21.42.103:8089","admin","temp1234")
dest_splunk.login()

coll_list = src_splunk.get_collection_list("nobody","testkvstore")
for coll in coll_list:
	if coll_list[coll]['sharing'] == 'app':
		print("Collection {}:".format(coll))

		dest_splunk.create_collection("nobody","testkvstore",coll)
		dest_splunk.set_collection_config("nobody","testkvstore",coll,src_splunk.get_collection_config("nobody","testkvstore",coll))
		dest_splunk.set_collection_data("nobody","testkvstore",coll,src_splunk.get_collection_data("nobody","testkvstore",coll))
