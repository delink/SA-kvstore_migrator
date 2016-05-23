#!/usr/bin/env python3

from kvstoremigrator import kvstoremigrator


src = {'url': 'https://172.21.42.102:8089', 'username': 'admin', 'password': 'temp124'}
dest = {'url': 'https://172.21.42.103:8089', 'username': 'admin', 'password': 'temp1234'}

migrator = kvstoremigrator(src,dest)

migrator.login()
