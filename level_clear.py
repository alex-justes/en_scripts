#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import pycurl
from io import BytesIO
import sys
import re
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
parser.add_option("--bonuses", action="store_true", dest="bonuses", default=False,
                  help="delete all bonuses")
parser.add_option("--tasks", action="store_true", dest="tasks", default=False,
                  help="delete all tasks")
parser.add_option("--clues", action="store_true", dest="clues", default=False,
                  help="delete all clues")
parser.add_option("--all", action="store_true", dest="all", default=False,
                  help="delete all")

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

if (options.all):
    options.bonuses = True
    options.tasks = True
    options.clues = True

delete_anything = False
if (options.bonuses or options.tasks or options.clues):
    delete_anything = True
if (options.verbose):
    print("Domain: ", options.domain)
    print("Cookie file: ", options.cookies)
    print("Level: ", options.level)
    print("GID: ", options.gid)
    print("Time: ", options.time)
    if (not delete_anything):
        print("Warning: nothing will be deleted!")
    if (options.bonuses):
        print("Bonuses will be deleted")
    if (options.tasks):
        print("Tasks will be deleted")
    if (options.clues):
        print("Clues will be deleted")

if (not delete_anything):
    sys.exit()

# Retrieve level to parse
url = "http://"+options.domain+"/Administration/Games/LevelEditor.aspx?gid="+options.gid+"&level="+options.level
buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(c.FOLLOWLOCATION, True)
c.setopt(c.COOKIEFILE, options.cookies)
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

content = str(buffer.getvalue())

tasks = []
clues = []
bonuses = []

if (options.tasks):
    tasks = re.findall(r'tid=(\d+)', content)
    if (not options.quiet):
        print("Tasks: ", tasks)
if (options.clues):
    clues = re.findall(r'prid=(\d+)', content)
    if (not options.quiet):
        print("Clues: ", clues)
if (options.bonuses):
    bonuses = re.findall(r'bonus=(\d+)', content)
    if (not options.quiet):
        print("Bonuses: ", bonuses)

if (options.fake):
    sys.exit()


random.seed()

for t in tasks:
    if (not options.quiet):
        print("Delete task ", t, " on level ", options.level)
    url = "http://"+options.domain+"/Administration/Games/TaskEdit.aspx?action=TaskDelete&gid="+options.gid+"&level="+options.level+"&tid="+t
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.COOKIEFILE, options.cookies)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    t = random.randint(0, options.time)
    if (not options.quiet):
        print("Sleep for: ",t, " seconds")
    time.sleep(t)

for cl in clues:
    if (not options.quiet):
        print("Delete clue ", cl, " on level ", options.level)
    url = "http://"+options.domain+"/Administration/Games/PromptEdit.aspx?action=PromptDelete&gid="+options.gid+"&level="+options.level+"&prid="+cl
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.COOKIEFILE, options.cookies)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    t = random.randint(0, options.time)
    if (not options.quiet):
        print("Sleep for: ",t, " seconds")
    time.sleep(t)

for b in bonuses:
    if (not options.quiet):
        print("Delete bonus ", b, " on level ", options.level)
    url = "http://"+options.domain+"/Administration/Games/BonusEdit.aspx?action=delete&gid="+options.gid+"&level="+options.level+"&bonus="+b
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.COOKIEFILE, options.cookies)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    t = random.randint(0, options.time)
    if (not options.quiet):
        print("Sleep for: ",t, " seconds")
    time.sleep(t)
    



