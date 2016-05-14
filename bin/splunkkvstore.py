#####
# splunkkvstore.py - Class for manipulating kvstore collections in Splunk
#####

import requests
requests.packages.urllib3.disable_warnings()

class splunkkvstore(object):

	# On instaniation, only collect the details. Do not do anything until login is called.
	def __init__(self,url,username,password):
		self.url = url;
		self.username = username;
		self.password = password;

	def __new__(cls,*args,**kwargs):
		obj = super().__new__(cls)
		return obj

	# Generic function to make an API call and return the results
	def api(self,method,api_endpoint,payload):
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
				results = self.session.post(self.url+api_endpoint,payload,verify=False)
			except:
				print("Unable to send to Splunk API: {}".format(sys.exc_info()[0]))
				return None
		elif method.lower() == 'delete':
			try:
				results = self.session.delete(self.url+api_endpoint,payload,verify=False)
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
	# This will return a list of base collection names
	def get_collection_list(self,owner_scope,app_scope):
		if not owner_scope:
			owner_scope = "-"
		if not app_scope:
			app_scope = "-"

		# http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTkvstore
		api_endpoint = "/servicesNS/{}/{}/storage/collections/config?output_mode=json".format(owner_scope,app_scope)

		get_coll_list_request = self.api("GET",api_endpoint,"")

		results = get_coll_list_request.json()
		coll_list = []
		for entry in results['entry']:
			coll_list.append(entry['id'])

		return coll_list
