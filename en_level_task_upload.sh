#!/bin/bash

#DOMAIN="demo.en.cx"
#COOKIEFILE="demo_cookies.txt"
#LID="9"
#GID="25286"
#TASKFILE="testtask"

DOMAIN=${1}
COOKIEFILE=${2}
LID=${3}
GID=${4}
TASKFILE=${5}

TASK=$(cat ${TASKFILE})

curl --data-urlencode "forMemberID=0" \
     --data-urlencode "inputTask=${TASK}" \
     --cookie "${COOKIEFILE}" \
	 --location \
	 "http://${DOMAIN}/Administration/Games/TaskEdit.aspx?gid=${GID}&level=${LID}" >/dev/null 2>/dev/null

echo Upload task ${TASKFILE} to level ${LID}

