#!/bin/bash

### Begin user variables
interval=$1
pinIdArr=(7 11 12 13 15 16 18 22)
bcmGpioArr=(4 17 18 27 22 23 24 25)
### End user variables


### Begin table header
echo
echo -e "Date\t\tpin(stat)\t ..."
for (( i=0; $i < 80; i=$i+1 ))
do
	echo -en "-"
done
echo
### End table header


### Begin Pin status
while true
do 
	echo -en "["`date +%H:%M:%S`"]\t"
	for (( i=0; $i < ${#pinIdArr[@]}; i=$i+1 ))
	do
		echo -en ${pinIdArr[i]}"("`gpio -g read ${bcmGpioArr[i]}`")\t"
	done
	echo ""
	if [ $interval ]; then
		sleep $interval
	else
		sleep 2
	fi
done
### End Pin status
