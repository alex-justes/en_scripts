#!/bin/bash

DOMAIN="demo.en.cx"
COOKIEFILE="demo_cookies.txt"
GID="25286"
TEMPFILE="temp.html"

LISTFILE="list.txt"

LIST=$(cat ${LISTFILE} | tr '\n' ' ')

for l in ${LIST}; do
	LEVEL=$(echo ${l} | gawk 'match($0, /([0-9]+)=/, a) {print a[1]}')
	DIR=$(echo ${l} | gawk 'match($0, /[0-9]+=(.+)/, a) {print a[1]}')
	echo level ${LEVEL} in ${DIR}
	TASK="${DIR}/task"
	CLUE1="${DIR}/clue_1"
	CLUE2="${DIR}/clue_2"
	CLUE3="${DIR}/clue_3"
	./en_level_clear.sh ${DOMAIN} ${COOKIEFILE} ${LEVEL} ${GID} ${TEMPFILE}
	sleep $[ ( $RANDOM % 10 )  + 1 ]s
	./en_level_task_upload.sh ${DOMAIN} ${COOKIEFILE} ${LEVEL} ${GID} ${TASK}
	sleep $[ ( $RANDOM % 10 )  + 1 ]s
	./en_level_clue_upload.sh ${DOMAIN} ${COOKIEFILE} ${LEVEL} ${GID} ${CLUE1} 0 0 0 10
	sleep $[ ( $RANDOM % 10 )  + 1 ]s
	./en_level_clue_upload.sh ${DOMAIN} ${COOKIEFILE} ${LEVEL} ${GID} ${CLUE2} 0 0 0 20
	sleep $[ ( $RANDOM % 10 )  + 1 ]s
	./en_level_clue_upload.sh ${DOMAIN} ${COOKIEFILE} ${LEVEL} ${GID} ${CLUE3} 0 0 0 30
	sleep $[ ( $RANDOM % 10 )  + 1 ]s
done



