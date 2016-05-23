#####
# kvstoremigrator.py - Class for cloning and migrating kvstore content
#                      between Splunk instances.
#####

from splunkkvstore import splunkkvstore

class kvstoremigrator(object):

	# On init, receive two dicts containing login details for each
	# Splunk instance. Use them to create two instances of splunkkvstore
	def __init__(self,src_splunk_details,dest_splunk_details):
		self.src_splunk_details = src_splunk_details
		self.dest_splunk_details = dest_splunk_details
		self.src_splunk = splunkkvstore(src_splunk_details['url'],src_splunk_details['username'],src_splunk_details['password'])
		self.dest_splunk = splunkkvstore(dest_splunk_details['url'],dest_splunk_details['username'],dest_splunk_details['password'])

	# Execute logins on both Splunk instances and make sure we are
	# good to go on both of them
	def login(self):

		try:
			self.src_splunk.login()
		except:
			raise

		try:
			self.dest_splunk.login()
		except:
			raise

		return None

