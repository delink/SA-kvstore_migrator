# kvstore_migrator.py

import sys
import splunkkvstore

# Introspection routine (eventually)
def do_scheme():
	pass

# Validation routine (eventually)
def validate_arguments():
	pass


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
		do_the_thing()

	sys.exit(0)
