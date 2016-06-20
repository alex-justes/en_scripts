#!/usr/bin/python

import sys
import re
import os

fileName = sys.argv[1]
acc = ""

with open(fileName) as f:
    for line in f:
        rtask = re.search(r'<!-- Задание (\d+) -->', line)
        rclue = re.search(r'<!-- Подсказка (\d+) -->', line)
        rcode = re.search(r'<!-- (.+) — (\d+) минут -->', line)
        rcomment = re.search(r'<!--.*-->', line)
        isTask = rtask != None
        isClue = rclue != None
        isComment = rcomment != None
        isCode = rcode != None

        if (isTask):
            if (acc != ""):
                print("flush clue3")
                ff = open("./levels/"+task+"/clue_3",'w')
                ff.write(acc)
                ff.close

            acc=""
            task = rtask.group(1)
            print("task ", task, " started")
            if (not os.access("./levels/"+task, os.F_OK)):
                os.mkdir("./levels/"+task)
        elif (isCode):
            acc += rcode.group(1)+":"+rcode.group(2)+"\n"
            if (re.match(r'\d{10}',rcode.group(1))):
                ff = open("./levels/"+task+"/bonus",'w')
                ff.write(acc)
                ff.close
                acc = ""
               
        elif (isClue):
            clue = rclue.group(1)
            if (clue == "1"):
                print("flush task")
                ff = open("./levels/"+task+"/task",'w')
                ff.write(acc)
                ff.close
            elif (clue == "2"):
                print("flush clue1")
                ff = open("./levels/"+task+"/clue_1",'w')
                ff.write(acc)
                ff.close
            elif (clue == "3"):
                print("flush clue2")
                ff = open("./levels/"+task+"/clue_2",'w')
                ff.write(acc)
                ff.close
            acc = ""
        elif (not isComment):
            acc += line
        else:
            print("Comment: ", rcomment.group(0))

print("flush clue3")
ff = open("./levels/"+task+"/clue_3",'w')
ff.write(acc)
ff.close
