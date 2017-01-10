#!/usr/bin/env python3

from kvstoremigrator import kvstoremigrator


src = {'url': 'https://192.168.134.10:8089', 'username': 'admin', 'password': 'temp1234'}
#src = {'url': 'https://192.168.134.10:8089', 'session_key': 'blTJ8oxwu_SKprpH5^q_aJxsiG2iTeLXN2KhZzxwM5TWNEKL5pU5HoM91cY0VakYPZ91Uu5_ED4Qf3pQqNflbpYjYaErHSqraZnmt8dLGA3LOv0'}
dest = {'url': 'https://192.168.134.11:8089', 'username': 'admin', 'password': 'temp1234'}

migrator = kvstoremigrator(src,dest)

migrator.login()

src_collections = migrator.src_splunk.get_collection_list("-","SA-kvstore_migrator_testapp")
dest_collections = migrator.dest_splunk.get_collection_list("-","SA-kvstore_migrator_testapp")
delete_coll_request = migrator.dest_splunk.delete_collection_data("admin","SA-kvstore_migrator_testapp","testcoll")
