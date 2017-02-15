TO-DO List for SA-kvstore_migrator
==================================

Core Functionality
------------------

* Function do_the_thing() needs to do something besides parse configuration (haha).
* Perhaps allow the app context to be populated as a drop-down by dynamically generating the scheme XML?


Logging
-------

* Determine a concrete and useful set of things to log at the INFO level.
* Determine how to alter the error in the red bar from saying "Script exited with error code 1".


Configuration
-------------

* Put attribute "password" into the secure credentials storage thingy Splunk has.
* Make the interval the migration runs something configurable rather than run-once.

Testing
-------

* Create standard app for creating and populating a collection from a search to be used for comparison on the local side.

