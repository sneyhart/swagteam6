#!/bin/bash

for x in $(seq 1 1 100) ; do
	if [ "$x" = "1" ] ; then
		cat clus$x > kohonen_combine.txt;
	else
		cat clus$x >> kohonen_combine.txt;
	fi
done
wait
