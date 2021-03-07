#!/usr/bin/env bash

today=`date +%Y-%m-%d`

if [ $# -eq 0 ]
then
	echo "Need filepath to SD Card images"
	exit 1
else
	SD=$1
fi

if [ ! -d /home/daemoneye/Pictures/${today} ]
then
	echo "Creating directory called ${today}"
	mkdir /home/daemoneye/Pictures/${today}
fi

mv -v $SD/*CR2 /home/daemoneye/Pictures/${today}

exit 1
