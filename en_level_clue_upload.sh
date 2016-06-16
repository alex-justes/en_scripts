#!/bin/bash

#DOMAIN="demo.en.cx"
#COOKIEFILE="demo_cookies.txt"
#LID="9"
#GID="25286"
#CLUEFILE="testtask"
#DAYS=1
#HOURS=2
#MINUTES=3
#SECONDS=5

DOMAIN=${1}
COOKIEFILE=${2}
LID=${3}
GID=${4}
CLUEFILE=${5}
DAYS=${6}
HOURS=${7}
MINUTES=${8}
SECONDS=${9}

CLUE=$(cat ${CLUEFILE})
curl --data-urlencode "forMemberID=0" \
	 --data-urlencode "NewPromptTimeoutDays=${DAYS}" \
	 --data-urlencode "NewPromptTimeoutHours=${HOURS}" \
	 --data-urlencode "NewPromptTimeoutMinutes=${MINUTES}" \
	 --data-urlencode "NewPromptTimeoutSeconds=${SECONDS}" \
     --data-urlencode "NewPrompt=${CLUE}" \
     --cookie "${COOKIEFILE}" \
	 --location \
	 "http://${DOMAIN}/Administration/Games/PromptEdit.aspx?gid=${GID}&level=${LID}" >/dev/null 2>/dev/null

echo Upload clue ${CLUEFILE} to level ${LID}

