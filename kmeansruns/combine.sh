#!/bin/bash

for x in $(seq 1 1 100) ; do
	if [ "$x" = "1" ] ; then
		cat clus$x > kmeans_combine.txt;
	else
		cat clus$x >> kmeans_combine.txt;
	fi
done
wait
