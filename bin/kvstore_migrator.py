# kvstore_migrator.py

import sys
import logging
import xml.dom.minidom
from splunkkvstore import splunkkvstore

# Introspection scheme to supply description and argument details.
def do_scheme():
	logging.debug("do_scheme(): Printing out scheme XML.")
	print("""<scheme>
	<title>KVStore Migrator</title>
	<description>Migrate KVStore contents from a remote Splunk instance to this one.</description>
	<use_external_validation>true</use_external_validation>
	<streaming_mode>simple</streaming_mode>
	<endpoint>
		<args>
			<arg name="remote_uri">
				<title>Remote Splunk URI</title>
				<description>URI of remote Splunk REST API to pull data from.</description>
			</arg>
			<arg name="user">
				<title>Remote Username</title>
				<description>Username of source Splunk REST API to pull data from.</description>
			</arg>
			<arg name="password">
				<title>Remote Splunk Password</title>
				<description>Password of source Splunk REST API to pull data from.</description>
			</arg>
			<arg name="app_context">
				<title>Splunk App Context</title>
				<description>App context to use for finding the collection list to migrate.</description>
			</arg>
		</args>
	</endpoint>
</scheme>
""")

# Validation routine for checking credentials to local Splunk and remote Splunk
def validate_arguments():
	# Pull configuration from input XML (error checking in function)
	logging.debug("validate_arguments(): Start.")
	config = get_config("validation")

	# Verify connection to remote splunk instance before saving configuration
	try:
		logging.debug("validate_arguments(): Attempting connection to remote Splunk instance at {}".format(config['remote_uri']))
		src_splunk = splunkkvstore(config['remote_uri'],config['user'],config['password'])
		src_splunk.login()
	except Exception,e:
		raise Exception,"Unable to connect to {}: {}".format(config['remote_uri'],str(e))

	# Looks good!
	logging.info("Connection to {} succeeded.".format(config['remote_uri']))
	pass

# Quick check to see if a key is defined and populated with a non-empty value
def check_for_empty(config, param):
	logging.debug("check_for_empty(): Checking '{}'.".format(param))
	if param not in config or config[param] == "":
		raise Exception, "Invalid configuration, attribute '{}' is missing from configuration.".format(param)
	pass

# Parse input configuration XML from Splunk for the module input
# Testing: /opt/splunk/bin/splunk cmd splunkd print-modinput-config kvstore_migrator kvstore_migrator://<stanza_name>
def get_config(type):
	logging.debug("get_config(): Start.")
	# Expected values in the resulting config dict
	config = {'name': '', 'server_ui': '', 'session_key': '', 'remote_uri': '', 'user': '', 'password': '', 'app_context': ''}

	# Pull the XML from STDIN and run it through parsing.
	try:
		logging.info("Loading configuration for {}.".format(type))
		logging.debug("get_config(): Reading configuration from STDIN.")
		config_str = sys.stdin.read()

		logging.debug("get_config(): Parsing XML configuration from STDIN.")
		doc = xml.dom.minidom.parseString(config_str)
		root = doc.documentElement

		if type == "modinput":
			logging.debug("get_config(): Parsing out server_uri from config XML.")
			server_uri = root.getElementsByTagName("server_uri")[0]
			if server_uri:
				config['server_uri'] = server_uri

			logging.debug("get_config(): Parsing out session_key from config XML.")
			session_key = root.getElementsByTagName("session_key")[0]
			if session_key:
				config['session_key'] = session_key

			logging.debug("get_config(): Parsing out configuration from config XML.")
			conf_node = root.getElementsByTagName("configuration")[0]
			if conf_node:
				logging.debug("get_config(): Parsing out stanza from config XML.")
				stanza = conf_node.getElementsByTagName("stanza")[0]

		elif type == "validation":
			logging.debug("get_config(): Parsing out item from config XML.")
			stanza = root.getElementsByTagName("item")[0]

		else:
			logging.debug("get_config(): Unknown type while attempting to parse config XML. Prepare for impact.")

		if stanza:
			logging.debug("get_config(): Getting name from the stanza section of config XML.")
			stanza_name = stanza.getAttribute("name")
			if stanza_name:
				config['name'] = stanza_name
				logging.debug("get_config(): Retrieving params array from the item/configuration stanza in config XML.")
				params = stanza.getElementsByTagName("param")
				for param in params:
					param_name = param.getAttribute("name")
					logging.debug("get_config(): Parsing out param '{}' from config XML.".format(param_name))
					if param_name and param.firstChild and param.firstChild.nodeType == param.firstChild.TEXT_NODE:
						data = param.firstChild.data
						config[param_name] = data

		# Validate required parameters are in the config dict
		check_for_empty(config,"remote_uri")
		check_for_empty(config,"user")
		check_for_empty(config,"password")
		check_for_empty(config,"app_context")

		# If this is a real run of the modular input, verify we have credentials for ourself.
		if type == "modinput":
			check_for_empty(config,"server_uri")
			check_for_empty(config,"session_key")

	except Exception,e:
		raise Exception, "Error getting Splunk configuration via STDIN: {}".format(str(e))

	# We did it! Send the dict back to whoever asked for it.
	logging.info("Loading configuration succeeded.")
	return config

def do_the_thing():
	logging.debug("do_the_thing(): Start.")

	# Get the config from incoming XML.
	config = get_config("modinput")

	# Setup API connection to the local Splunk instance
	try:
		logging.debug("do_the_thing(): Attempting connection to local Splunk instance at {}".format(config['server_uri']))
		dest_splunk = splunkkvstore(config['server_uri'],config['session_key'])
		dest_splunk.login()
	except Exception,e:
		raise Exception,"Unable to connect to {}: {}".format(config['server_uri'],str(e))

	# Looks good!
	logging.info("Connection to {} succeeded.".format(config['server_uri']))


	# Setup API connections to the remote Splunk instance
	try:
		logging.debug("do_the_thing(): Attempting connection to remote Splunk instance at {}".format(config['remote_uri']))
		src_splunk = splunkkvstore(config['remote_uri'],config['user'],config['password'])
		src_splunk.login()
	except Exception,e:
		raise Exception,"Unable to connect to {}: {}".format(config['remote_uri'],str(e))

	# Looks good!
	logging.info("Connection to {} succeeded.".format(config['remote_uri']))

	# Grab the list of collections to migrate based on app_context
	try:
		logging.debug("do_the_thing(): Retrieving list of collections from app {}".format(config['app_context']))
		coll_list = src_splunk.get_collection_list("",config['app_context'])
	except Exception,e:
		raise Exception,"Unable to get list of collections from remote Splunk: {}".format(str(e))

	# Process each collection as it comes through, skipping the system-based collections.
	for coll in coll_list:
		logging.debug("do_the_thing(): Starting processing on collection {}".format(coll))

		# There are collections defined in the system itself. We probably don't want to copy these.
		if coll_list[coll]['sharing'] == 'system':
			logging.debug("do_the_thing(): Skipping collection because it is built-in to Splunk.")
			continue

		# Retrieve the configuration from the collection.
		try:
			logging.debug("do_the_thing(): Retrieving collection configuration for {}".format(coll))
			coll_config = src_splunk.get_collection_config("nobody",config['app_context'],coll)
		except Exception,e:
			raise Exception,"Unable to get collection configuration: {}".format(str(e))

		# Retrieve the data from the collection.
		try:
			logging.debug("do_the_thing(): Retrieving collection data for {}".format(coll))
			coll_data = src_splunk.get_collection_data("nobody",config['app_context'],coll)
		except Exception,e:
			raise Exception,"Unable to get collection data: {}".format(str(e))

		# If we're still running, we have the goods. Load them up into the local instance.

		# Configuration
		try:
			logging.debug("do_the_thing(): Loading collection configuration for {}".format(coll))
			dest_splunk.set_collection_config("nobody",config['app_context'],coll,coll_config)
		except Exception,e:
			raise Exception,"Unable to load collection configuration: {}".format(str(e))

		# Data
		try:
			logging.debug("do_the_thing(): Loading collection data for {}".format(coll))
			dest_splunk.set_collection_config("nobody",config['app_context'],coll,coll_data)
		except Exception,e:
			raise Exception,"Unable to load collection data: {}".format(str(e))

if __name__ == '__main__':
	# set up logging suitable for splunkd consumption
	logging.root
	logging.root.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(levelname)s %(message)s')
	handler = logging.StreamHandler(stream=sys.stderr)
	handler.setFormatter(formatter)
	logging.root.addHandler(handler)

	# process command line arguments
	if len(sys.argv) > 1:
		if sys.argv[1] == "--scheme":
			logging.debug("Getting ready to dump the scheme.")
			do_scheme()
		elif sys.argv[1] == "--validate-arguments":
			logging.debug("Getting ready to validate arguments.")
			validate_arguments()
		else:
			pass

	else:
		logging.debug("Getting ready to run a migration.")
		do_the_thing()

	sys.exit(0)
