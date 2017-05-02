#!/bin/bash

for x in $(seq 1 1 100) ; do
	echo "x is $x" ;
	./wta $1 $x > wtaruns/clus$x &
done
wait
