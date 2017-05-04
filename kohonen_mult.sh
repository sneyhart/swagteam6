#!/bin/bash

for x in $(seq 0 10 90) ; do
	for i in $(seq $x 1 $(($x + 10))) ; do
		echo "x is $i" ;
		./kohonen $1 $i > kohonenruns/clus$i &
	done
	wait
done
wait
