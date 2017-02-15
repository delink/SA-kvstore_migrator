#!/bin/bash

# Script to generate the files to be read by the forwarder for testing the SEC stack.

# Space-separated list of the number of events to generate for each test run
event_test_run="50000"

# Number of seconds to pause between data writes
#pause_time_divisor=`echo $event_test_run | awk '{print $1}'`
pause_time_divisor=1

# Number of indexers
IDX=1

# Once the files have been generated, stop doing anything at all.
if [ -f /tmp/disable-generate-event-files ]; then
	exit 0
fi

# Remove the files if they exist
for ((i=1;i<=${IDX};++i)); do
	rm -f /tmp/test-indexer-${i}.log
done

j=0
for EVTS in ${event_test_run}; do
	# Generate configured lines of data per indexer
	for ((i=1;i<=${IDX};++i)); do
		# wait for data to finish
		sleep $(($j / $pause_time_divisor * 4))

		# Generate the current time to the nanosecond for the file writes
		starttime=`date "+%Y-%m-%d %H:%M:%S.%N %z"`

		# Generate a splunk-friendly log file that is identical across three indexers
		output="$starttime indexer_name=indexer-$i total_events=$EVTS log_seq="
		for ((j=1;j<=${EVTS};++j)); do
			echo "${output}${j}" >> /tmp/test-indexer-${i}.log
		done
	done
done

# Check all log files to be sure they were written
retval=0
for ((i=1;i<=${IDX};++i)); do
	if [ ! -f /tmp/test-indexer-${i}.log ]; then
		retval=$(($retval + 1))
	fi
done
if [ "$retval" = 0 ]; then
	touch /tmp/disable-generate-event-files
fi
