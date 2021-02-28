#!/bin/sh

irc='daemoneye@daemo.nz'

if [ $# -eq 0 ]
then
	echo "Need files to upload"
	exit 1
fi

scp $@ $irc:~

exit 0
