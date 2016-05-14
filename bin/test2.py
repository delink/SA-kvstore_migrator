#!/usr/bin/env python3

# Second attempt at test.py, now with the new library

from splunkkvstore import splunkkvstore

src_splunk = splunkkvstore("https://172.21.42.103:8089","admin","temp1234")
src_splunk.login()
print(src_splunk.get_collection_list("nobody","testkvstore"))
