#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import pycurl
from io import BytesIO
import sys
import re
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
parser.add_option("--on_levels", action="store", type="string", dest="on_levels", default="",
                  help="activete bonus on these levels (example: '1;3;4')")
parser.add_option("--ftask", action="store", type="string", dest="task", default="",
                  help="file with task")
parser.add_option("--fhelp", action="store", type="string", dest="help", default="",
                  help="file with help")
parser.add_option("-n", "--name", action="store", type="string", dest="name", default="",
                  help="specify name")
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
if (error):
	sys.exit()

if (options.verbose):
	print("Domain: ", options.domain)
	print("Cookie file: ", options.cookies)
	print("Level: ", options.level)
	print("GID: ", options.gid)
	print("Time: ", options.time)


# Retrieve level to parse
url = "http://"+options.domain+"/Administration/Games/BonusEdit.aspx?gid="+options.gid+"&level="+options.level+"&action=add"
buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(c.COOKIEFILE, options.cookies)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

random.seed()
t = random.randint(0, options.time)
if (not options.quiet):
    print("Sleep for: ",t, " seconds")
    time.sleep(t)


content = str(buffer.getvalue())

ids = re.findall(r'name="(level_\d+)"', content)
nums = re.findall(r'LevelNum">(\d+)<', content)
levels = {}
for l in nums:
    levels[l] = ids[int(l) - 1]


task = ""
with open(options.task, 'r') as content_file:
    task = content_file.read()
help = ""
with open(options.help, 'r') as content_file:
    help = content_file.read()

url = "http://"+options.domain+"/Administration/Games/BonusEdit.aspx?gid="+options.gid+"&level="+options.level+"&bonus=0&action=save"

post_data = {"ddlBonusFor" : "0", 
             "txtBonusName" : options.name,
             "txtTask" : task,
             "rbAllLevels" : "1",
             "txtHours" : options.hours,
             "txtMinutes" : options.minutes,
             "txtSeconds" : options.seconds,
             "txtHelp" : help}

answers = options.answers.split(";")
i = 1
for a in answers:
    post_data["answer_-"+str(i)] = a
    i += 1
levels_to_add = options.on_levels.split(";")
for l in levels_to_add:
    post_data[levels[l]] = l

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
    print("Upload bonus ", options.name, " on levels ", options.on_levels, " time: ", options.days, " - ", options.hours, ":", options.minutes, ":", options.seconds)
    print("Sleep for: ",t, " seconds")
    time.sleep(t)

