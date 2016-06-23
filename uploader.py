#!/usr/bin/python

#TODO: Check if cookie-file exists
#TODO: Somehow check correctness

import sys
import re
import os
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False,
                  help="verbose output")
parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False,
                  help="tssss...")
parser.add_option("-d", "--domain", action="store", type="string", dest="domain", default="demo.en.cx",
                  help="set domain [demo.en.cx]")
parser.add_option("-c", "--cookies", action="store", type="string", dest="cookies", default="cookies.txt",
                  help="set file with auth-cookies [cookies.txt]")
parser.add_option("-g", "--gid", action="store", type="string", dest="gid", default="",
                  help="set gid")
parser.add_option("-f", "--file", action="store", type="string", dest="file", default="",
                  help="specify input file")
parser.add_option("-t", "--time", action="store", type="int", dest="time", default="0",
                          help="specify random delay in seconds between queries [0]")

(options, args) = parser.parse_args(sys.argv)

error = False
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
    print("GID: ", options.gid)
    print("Input file: ", options.file)


with open(options.file) as f:
    for line in f:
        if (line[0] == "#"):
            print("Skip: ", line)
        else:
            s = re.search(r'(\d+)=(.+)', line)
            if (s != None):
                level = s.group(1)
                path = s.group(2)
                print("Level: ", level, " Path: ", path)
                task_path = path + "/task"
                clue_1_path = path + "/clue_1"
                clue_2_path = path + "/clue_2"
                clue_3_path = path + "/clue_3"
                bonus_path = path + "/bonus"

                clear = "./level_clear.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " --all" + " -d " + options.domain
                load_task = "./level_upload_task.py -l " + level + " -g " + options.gid + " -t " + str(options.time) +  " -f " + task_path + " -d " + options.domain
                load_clue_1 = "./level_upload_clue.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " -f " + clue_1_path + " --hours 1"  + " -d " + options.domain
                load_clue_2 = "./level_upload_clue.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " -f " + clue_2_path + " --hours 2"  + " -d " + options.domain
                load_clue_3 = "./level_upload_clue.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " -f " + clue_3_path + " --hours 3 --minutes 30"  + " -d " + options.domain
                answers = ""
                bonuses = []
                bid = 1
                with open(bonus_path) as fb:
                    for b in fb:
                        rb = re.search(r'(.+):(.+)', b)
                        ss = "./level_upload_bonus.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " --fhelp " + bonus_path + "_help_"+str(bid) + \
                                " --minutes " + rb.group(2) + " --on_levels " + level + " --ftask " + bonus_path + "_task_"+str(bid) + " -d " + options.domain
                        pointID = (int(level)*5 - 5) + bid
                        if (bid == 6):
                            ss += " --answers '" + rb.group(1) + "'" + " --name 'Категория'"
                            answers = "./level_upload_answer.py -l " + level + " -g " + options.gid + " -t " + str(options.time) + " --answers '" + rb.group(1)  + "'" + " -d " + options.domain
                        else:
                            ss += " --answers '" + rb.group(1) + ";пп" + rb.group(1) + "'" + " --name 'Точка " + str(pointID) + "'"
                        bid += 1
                        bonuses.append(ss)

                print(clear)
                print(load_task)
                print(load_clue_1)
                print(load_clue_2)
                print(load_clue_3)
                for b in bonuses:
                    print(b)
                print(answers)

                os.system(clear)
                os.system(load_task)
                os.system(load_clue_1)
                os.system(load_clue_2)
                os.system(load_clue_3)
                for b in bonuses:
                    os.system(b)
                os.system(answers)
        

