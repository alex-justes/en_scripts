#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import pycurl
import sys
from io import BytesIO
from optparse import OptionParser
from urllib.parse import urlencode
import time
import random

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="verbose output")
parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
                  help="tssss...")
parser.add_option("-d", "--domain", action="store", type="string", dest="domain", default="demo.en.cx",
                  help="set domain [demo.en.cx]")
parser.add_option("-c", "--cookies", action="store", type="string", dest="cookies", default="cookies.txt",
                  help="set file with auth-cookies [cookies.txt]")
parser.add_option("-l", "--level", action="store", type="string", dest="level", default="",
                  help="set level")
parser.add_option("-g", "--gid", action="store", type="string", dest="gid", default="",
                  help="set gid")
parser.add_option("-t", "--time", action="store", type="int", dest="time", default="0",
                  help="specify random delay in seconds between queries [0]")
parser.add_option("-f", "--file", action="store", type="string", dest="file", default="",
                  help="specify input file")

parser.add_option("--days", action="store", type="string", dest="days", default="0",
                  help="specify days")
parser.add_option("--hours", action="store", type="string", dest="hours", default="0",
                  help="specify hours")
parser.add_option("--minutes", action="store", type="string", dest="minutes", default="0",
                  help="specify minutes")
parser.add_option("--seconds", action="store", type="string", dest="seconds", default="0",
                  help="specify seconds")

(options, args) = parser.parse_args(sys.argv)

error = False
if (options.level == ""):
    print("Error: You must specify level!")
    error = True
if (options.gid == ""):
    print("Error: You must specify gid!")
    error = True
if (options.file == ""):
    print("Error: You must specify input file!")
if (error):
    sys.exit()

if (options.verbose):
    print("Domain: ", options.domain)
    print("Cookie file: ", options.cookies)
    print("Level: ", options.level)
    print("GID: ", options.gid)
    print("Input file: ", options.file)

random.seed()

content = ""
with open(options.file, 'r') as content_file:
    content = content_file.read()

url = "http://"+options.domain+"/Administration/Games/PromptEdit.aspx?gid="+options.gid+"&level="+options.level

post_data = {"ForMemberID" : "0", 
             "NewPromptTimeoutDays" : options.days,
             "NewPromptTimeoutHours" : options.hours,
             "NewPromptTimeoutMinutes" : options.minutes,
             "NewPromptTimeoutSeconds" : options.seconds,
             "NewPrompt" : content}
postfields = urlencode(post_data)

buffer = BytesIO()

c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(c.POSTFIELDS, postfields)
c.setopt(c.COOKIEFILE, options.cookies)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

t = random.randint(0, options.time)
if (not options.quiet):
    print("Upload clue " +options.file+" to level "+options.level)
    print("Sleep for: ",t, " seconds")
time.sleep(t)

