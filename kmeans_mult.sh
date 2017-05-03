#!/bin/bash

for x in $(seq 0 10 90) ; do
	for i in $(seq $x 1 $(($x + 10))) ; do
		echo "x is $i" ;
		./kmeans $1 $i > kmeansruns/clus$i &
	done
	wait
done
wait
