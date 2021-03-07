#!/usr/bin/env bash

today=`date +%Y-%m-%d`
pictures="/home/daemoneye/Piuctures"

if [ $# -eq 0 ]
then
	echo "Need filepath to SD Card images"
	exit 1
else
	SD=$1
fi

if [ ! -d ${pictures}/${today} ]
then
	echo "Creating directory called ${today}"
	mkdir ${pictures}/${today}
fi

mv -v $SD/*CR2 ${pictures}/${today}

exit 1
