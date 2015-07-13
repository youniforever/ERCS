#!/bin/bash

function help() {
	echo -e "Usages) "$0"\t[...]\t[...]\t\t[description]"
	echo -e "\t\t\t\t\tserver\tstart \t\t# start server"
	echo -e "\t\t\t\t\tserver\tstop  \t\t# stop server"
	echo -e "\t\t\t\t\tserver\trestart \t# restart server"
	echo -e "\t\t\t\t\tclient\tstart \t\t# start client"
	echo -e "\t\t\t\t\tclient\tstop  \t\t# stop client"
	echo -e "\t\t\t\t\tclient\trestart \t# restart client"
	echo -e "\t\t\t\t\tps            \t\t# show process list"
	exit 1
}

function startServer() {
	isErcsAgentServer=`ps -ef | grep ercs-server-daemon | grep -v grep | wc -l`
	if [ $isErcsAgentServer -eq 0 ]; then
		source $base/server/bin/activate
		python $base/server/__init__.py --ercs-server-daemon &
	fi
}

function stopServer() {
	ps -ef | grep ercs-server-daemon | grep -v grep | awk '{print $2}' | while read pId
	do
		kill -9 $pId
	done
}

function startClient() {
	isErcsAgentClient=`ps -ef | grep ercs-client-daemon | grep -v grep | wc -l`
	if [ $isErcsAgentClient -eq 0 ]; then
		source $base/client/bin/activate
		python $base/client/__init__.py --ercs-client-daemon &
	fi
}

function stopClient() {
	ps -ef | grep ercs-client-daemon | grep -v grep | awk '{print $2}' | while read pId
	do
		kill -9 $pId
	done
}

function showProcess() {
	ps -ef | grep ercs | grep -v grep
}



base="/usr/local/ERCS"
serviceName=$1
serviceMode=$2

if [[ ${#serviceName} > 0 ]]; then
	if [[ ${#serviceMode} > 0 ]]; then
		if [ $serviceName == "server" ]; then
			if [ $serviceMode == "start" ]; then
				startServer
			elif [ $serviceMode == "stop" ]; then
				stopServer
			elif [ $serviceMode == "restart" ]; then
				stopServer
				startServer
			else
				help
			fi
		elif [ $serviceName == "client" ]; then
			if [ $serviceMode == "start" ]; then
				startClient
			elif [ $serviceMode == "stop" ]; then
				stopClient
			elif [ $serviceMode == "restart" ]; then
				stopClient
				startClient
			else
				help
			fi
		else
			help
		fi
	else
		if [ $serviceName == "ps" ]; then
			showProcess
		else
			help
		fi
	fi
else
	help
fi 
