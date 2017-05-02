#!/bin/bash

for x in $(seq 1 1 100) ; do
	if [ "$x" = "1" ] ; then
		echo "-------For Number of clusters $x: -------" > wta_combine.txt
		cat clus$x >> wta_combine.txt;
	else
		echo "-------For Number of clusters $x: -------" >> wta_combine.txt
		cat clus$x >> wta_combine.txt;
	fi
done
wait
