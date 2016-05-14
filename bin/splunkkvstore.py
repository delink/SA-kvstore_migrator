#####
# splunkkvstore.py - Class for manipulating kvstore collections in Splunk
#####

import requests
import json
requests.packages.urllib3.disable_warnings()

class splunkkvstore(object):

	# On instaniation, only collect the details. Do not do anything until login is called.
	def __init__(self,url,username,password):
		self.url = url;
		self.username = username;
		self.password = password;

	# Generic function to make an API call and return the results
	def api(self,method,api_endpoint,*payload):
		if payload is None:
			payload == ""
		if method.lower() == 'get':
			try:
				results = self.session.get(self.url+api_endpoint,verify=False)
			except:
				print("Unable to retrieve from Splunk API: {}".format(sys.exc_info()[0]))
				return None
		elif method.lower() == 'post':
			try:
				results = self.session.post(self.url+api_endpoint,payload[0],verify=False,headers={"content-type":"application/json"})
			except:
				print("Unable to send to Splunk API: {}".format(sys.exc_info()[0]))
				return None
		elif method.lower() == 'delete':
			try:
				results = self.session.delete(self.url+api_endpoint,verify=False)
			except:
				print("Unable to delete in Splunk API: {}".format(sys.exc_info()[0]))
				return None
		else:
			raise ValueError("Unknown method: {}".format(method))
			return None

		return results

	# Retrieve the session key inside of a requests.Session() object and store it in the object.
	def login(self):

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTaccess
		api_endpoint = "/services/auth/login"
		creds_payload = { 'cookie': '1', 'username': self.username, 'password': self.password }

		self.session = requests.Session()
		login_request = self.api("POST",api_endpoint,creds_payload)
		return None

	# Get the list of collection names from a particular scope. Use "-" for no scope
	# This will return a dict with keys of base collection names and values as the acl dict
	def get_collection_list(self,owner_scope,app_scope):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config?output_mode=json".format(owner_scope,app_scope)

		get_coll_list_request = self.api("GET",api_endpoint)

		results = get_coll_list_request.json()
		coll_list = {}
		for entry in results['entry']:
			coll_list[entry['id'].split("/")[-1]] = entry['acl']

		return coll_list

	def create_collection(self,owner_scope,app_scope,coll_name):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config?output_mode=json".format(owner_scope,app_scope)
		payload = { 'name': coll_name }

		create_coll_request = self.api("POST",api_endpoint,payload)

		results = create_coll_request.json()

		return 0

	def delete_collection(self,owner_scope,app_scope,coll_name):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config/{}?output_mode=json".format(owner_scope,app_scope,coll_name)

		delete_coll_request = self.api("DELETE",api_endpoint)

		results = delete_coll_request.json()

		return 0

	# This method returns the collection's configuration as a JSON string
	def get_collection_config(self,owner_scope,app_scope,coll_name):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config/{}?output_mode=json".format(owner_scope,app_scope,coll_name)

		get_coll_config_request = self.api("GET",api_endpoint)

		return get_coll_config_request.text

	# This method returns the collection's data as a JSON string
	def get_collection_data(self,owner_scope,app_scope,coll_name):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/data/{}?output_mode=json".format(owner_scope,app_scope,coll_name)

		get_coll_data_request = self.api("GET",api_endpoint)

		return get_coll_data_request.text

	# This method sets the collection's configuration using the provided JSON string
	def set_collection_config(self,owner_scope,app_scope,coll_name,configuration):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config/{}?output_mode=json".format(owner_scope,app_scope,coll_name)
		payload = configuration

		set_coll_config_request = self.api("POST",api_endpoint,payload)

		return 0

	# This method sets the collection's data using the provided JSON string
	def set_collection_data(self,owner_scope,app_scope,coll_name,data):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/data/{}/batch_save?output_mode=json".format(owner_scope,app_scope,coll_name)
		payload = data

		set_coll_data_request = self.api("POST",api_endpoint,payload)

		return set_coll_data_request.text
