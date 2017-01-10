# kvstore_migrator.py

import sys
import logging
import xml.dom.minidom
from splunkkvstore import splunkkvstore

# Introspection scheme to supply description and argument details.
def do_scheme():
	print("""<scheme>
	<title>KVStore Migrator</title>
	<description>Migrate KVStore contents from one Splunk instance to another.</description>
	<use_external_validation>true</use_external_validation>
	<streaming_mode>simple</streaming_mode>
	<endpoint>
		<args>
			<arg name="source_splunk">
				<title>Source Splunk instance URL</title>
				<description>URL of source Splunk REST API to pull data from.</description>
			</arg>
			<arg name="user">
				<title>Source Splunk instance username</title>
				<description>Username of source Splunk REST API to pull data from.</description>
			</arg>
			<arg name="password">
				<title>Source Splunk instance password</title>
				<description>Password of source Splunk REST API to pull data from.</description>
			</arg>
		</args>
	</endpoint>
</scheme>
""")

# Validation routine (eventually)
def validate_arguments():
	# Pull configuration from input XML (error checking in function)
	config = get_config()

	# Verify connection to local splunk instance
	try:
		dest_splunk = splunkkvstore(config['server_uri'],config['session_key'])
		dest_splunk.login()
	except Exception,e:
		raise "Unable to connect to local Splunk instance API: {}".format(str(e))

	# Verify connection to remote splunk instance
	try:
		src_splunk = splunkkvstore(config['source_splunk'],config['user'],config['password'])
		src_splunk.login()
	except Exception,e:
		raise "Unable to connect to remote Splunk instance API: {}".format(str(e))

	# Looks good!
	pass

# Quick check to see if a key is defined and populated with a non-empty value
def check_for_empty(config, param):
	if param not in config or config[param] == "":
		raise Exception, "Invalid configuration, attribute '{}' is missing from configuration.".format(param)
	pass

# Parse input configuration XML from Splunk for the module input
# Testing: /opt/splunk/bin/splunk cmd splunkd print-modinput-config kvstore_migrator kvstore_migrator://<stanza_name>
def get_config():
	# Expected values in the resulting config dict
	config = {'name': '', 'server_ui': '', 'session_key': '', 'source_splunk': '', 'user': '', 'password': ''}

	# Pull the XML from STDIN and run it through parsing.
	try:
		config_str = sys.stdin.read()

		doc = xml.dom.minidom.parseString(config_str)
		root = doc.documentElement
		server_uri = root.getElementsByTagName("server_uri")[0]
		if server_uri:
			config['server_uri'] = server_uri
		session_key = root.getElementsByTagName("session_key")[0]
		if session_key:
			config['session_key'] = session_key
		conf_node = root.getElementsByTagName("configuration")[0]
		if conf_node:
			stanza = conf_node.getElementsByTagName("stanza")[0]
			if stanza:
				stanza_name = stanza.getAttribute("name")
				if stanza_name:
					config['name'] = stanza_name
					params = stanza.getElementsByTagName("param")
					for param in params:
						param_name = param.getAttribute("name")
						if param_name and param.firstChild and param.firstChild.nodeType == param.firstChild.TEXT_NODE:
							data = param.firstChild.data
							config[param_name] = data

		# Validate required parameters are in the config dict
		check_for_empty(config,"server_uri")
		check_for_empty(config,"session_key")
		check_for_empty(config,"source_splunk")
		check_for_empty(config,"user")
		check_for_empty(config,"password")
	except Exception,e:
		raise Exception, "Error getting Splunk configuration via STDIN: {}".format(str(e))

	# We did it! Send the dict back to whoever asked for it.
	return config

# Process arguments
if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == "--scheme":
			do_scheme()
		elif sys.argv[1] == "--validate-arguments":
			validate_arguments()
		else:
			pass

	else:
		#do_the_thing()
		pass

	sys.exit(0)
