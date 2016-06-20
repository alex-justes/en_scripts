#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import pycurl
from io import BytesIO
from urllib.parse import urlencode
import sys
import getpass
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="verbose output")
parser.add_option("-d", "--domain", action="store", type="string", dest="domain", default="demo.en.cx",
                  help="set domain [demo.en.cx]")
parser.add_option("-c", "--cookies", action="store", type="string", dest="cookies", default="cookies.txt",
                  help="set file with auth-cookies [cookies.txt]")
parser.add_option("-l", "--login", action="store", type="string", dest="login", default="",
                  help="set login")
parser.add_option("-p", "--password", action="store", type="string", dest="password", default="",
                  help="set password")

(options, args) = parser.parse_args(sys.argv)

if (options.verbose):
    print("Domain: ", options.domain)
    print("Cookie file: ", options.cookies)
    if (options.login != ""):
        print("Login: ", options.login)

if (options.login == ""):
    options.login = input("Login: ")
if (options.password == ""):
    options.password = getpass.getpass("Password: ")

url = "http://"+options.domain+"/Login.aspx"

post_data = {"Login" : options.login, "Password" : options.password}
postfields = urlencode(post_data)

buffer = BytesIO()

c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(c.POSTFIELDS, postfields)
c.setopt(c.COOKIEJAR, options.cookies)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

