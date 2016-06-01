#!/bin/bash

FILES="files.txt"
DOMAIN="66.en.cx"
COOKIEFILE="en_cookies.txt"
GID="24842"

if [ -z ${1} ];
then
	echo "You must specify domain!"
    exit 1
else
	DOMAIN=$1
fi

if [ -z ${2} ];
then
	echo "You must specify cookie-file!"
	exit 2
else
	 COOKIEFILE=$2
fi

if [ -z ${3} ];
then
	echo "You must specify file with images' names!"
	exit 3
else
	 FILES=$3
fi

if [ -z ${4} ];
then
	echo "You must specify GID!"
	exit 4
else
	 GID="$4"
fi

echo "Domain: $DOMAIN"
echo "Cookie-file: $COOKIEFILE"
echo "File-list: $FILES"
echo "GID: $GID"

FILES=$(cat $FILES)

function sendFiles {
	CMD="--cookie $COOKIEFILE $1 $URL >/dev/null"
	curl --cookie $COOKIEFILE \
	     $1 \
         "http://$DOMAIN/Administration/Games/FileUploader.aspx?gid=$GID" >/dev/null
}

i=1
CMD=''
for f in ${FILES}; do
	if [ ${i} -lt 11 ]
	then
		if [[ ${f:0:1} != '#' ]];
		then
			TMP="inputFile$i=@$f;filename=$f"
			CMD="$CMD -F $TMP"
			let i+=1
		fi
	else
		let i=1
		sendFiles "$CMD"
		CMD=''
	fi
done

if [ ! -z ${CMD+x} ];
then
	sendFiles "$CMD"
fi

