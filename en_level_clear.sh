#!/bin/bash

#DOMAIN="demo.en.cx"
#COOKIEFILE="demo_cookies.txt"
#LID="9"
#GID="25286"
#TEMPFILE="temp.html"

DOMAIN=${1}
COOKIEFILE=${2}
LID=${3}
GID=${4}
TEMPFILE=${5}

curl --cookie "${COOKIEFILE}" \
	--location \
	"http://${DOMAIN}/Administration/Games/LevelEditor.aspx?action=TaskDelete&gid=${GID}&level=${LID}" >${TEMPFILE} 2>/dev/null

TIDS=$(cat ${TEMPFILE} | gawk 'match($0, /tid=([0-9]+)/, a) {print a[1]}' | tr '\n' ' ')
PRIDS=$(cat ${TEMPFILE} | gawk 'match($0, /prid=([0-9]+)/, a) {print a[1]}' | tr '\n' ' ')

for t in ${TIDS}; do
	echo Delete task ${t} on level ${LID}
	curl --cookie "${COOKIEFILE}" \
		 --location \
		 "http://${DOMAIN}/Administration/Games/TaskEdit.aspx?action=TaskDelete&gid=${GID}&level=${LID}&tid=${t}" >/dev/null 2>/dev/null
done

for p in ${PRIDS}; do
	echo Delete clue ${p} on level ${LID}
	curl --cookie "${COOKIEFILE}" \
		--location \
		"http://${DOMAIN}/Administration/Games/PromptEdit.aspx?action=PromptDelete&gid=${GID}&level=${LID}&prid=${p}" >/dev/null 2>/dev/null
done

rm -f ${TEMPFILE}

