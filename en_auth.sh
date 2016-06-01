#!/bin/bash

DOMAIN="66.en.cx"
COOKIEFILE="en_cookies.txt"

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

echo -n 'Login: '
read LOGIN
echo -n 'Password: '
read -s PASSWORD
echo

echo "User: $LOGIN"
echo "Domain: $DOMAIN"
echo "Cookie-file: $COOKIEFILE"

curl --data-urlencode "Login=$LOGIN" \
	 --data-urlencode "Password=$PASSWORD" \
     --cookie-jar "$COOKIEFILE" \
	 --location \
	 "http://$DOMAIN/Login.aspx" >/dev/null

