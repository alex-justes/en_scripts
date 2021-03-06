#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import pycurl
from io import BytesIO
import sys
from urllib.parse import urlencode
from optparse import OptionParser
import time
import random

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="verbose output")
parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
                  help="tssss...")
parser.add_option("-f", "--fake", action="store_true", dest="fake", default=False,
                  help="just show, don't delete")
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

parser.add_option("--answers", action="store", type="string", dest="answers", default="",
                  help="set answers (example: 'test1;pptest1;test2')")


(options, args) = parser.parse_args(sys.argv)

error = False
if (options.level == ""):
    print("Error: You must specify level!")
    error = True
if (options.gid == ""):
    print("Error: You must specify gid!")
    error = True
if (error):
    sys.exit()

if (options.verbose):
    print("Domain: ", options.domain)
    print("Cookie file: ", options.cookies)
    print("Level: ", options.level)
    print("GID: ", options.gid)
    print("Time: ", options.time)



url = "http://"+options.domain+"/Administration/Games/LevelEditor.aspx?gid="+options.gid+"&level="+options.level

post_data = {"saveanswers" : "1"}

answers = options.answers.split(";")
i = 0
for a in answers:
    post_data["txtAnswer_"+str(i)] = a
    post_data["ddlAnswerFor_"+str(i)] = "0"
    i += 1

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
    print("Upload answers ", answers, " on level ", options.level)
    print("Sleep for: ",t, " seconds")
    time.sleep(t)

