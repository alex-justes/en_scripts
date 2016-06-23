#!/usr/bin/python

import sys
import re
import os

fileName = sys.argv[1]
acc = ""
code = 1

def chooseEnding( num ):
    rem = num % 10
    if (rem == 1 and num != 11):
        return "минута"
    elif ((rem == 2 or rem == 3 or rem == 4) and not (num == 12 or num == 13 or num == 14)):
        return "минуты"
    else:
        return "минут"

with open(fileName) as f:
    for line in f:
        rtask = re.search(r'<!-- Задание (\d+) -->', line)
        rclue = re.search(r'<!-- Подсказка (\d+) -->', line)
        rcode = re.search(r'<!-- (.+) — (\d+) минут.* -->', line)
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
                ff.close()

            acc=""
            task = rtask.group(1)
            code = 1
            print("task ", task, " started")
            if (not os.access("./levels/"+task, os.F_OK)):
                os.mkdir("./levels/"+task)
        elif (isCode):
            acc += rcode.group(1)+":"+rcode.group(2)+"\n"
            ff = open("./levels/"+task+"/bonus_help_"+str(code), 'w')
            ff.write(rcode.group(1))
            ff.close()
            ff = open("./levels/"+task+"/bonus_task_"+str(code),'w')
            ttime = int(rcode.group(2))
            ff.write(rcode.group(2)+" "+chooseEnding(ttime))
            ff.close()
            code += 1
            if (re.match(r'\d{10}',rcode.group(1))):
                ff = open("./levels/"+task+"/bonus",'w')
                ff.write(acc)
                ff.close()
                acc = ""
               
        elif (isClue):
            clue = rclue.group(1)
            if (clue == "1"):
                print("flush task")
                ff = open("./levels/"+task+"/task",'w')
                ff.write(acc)
                ff.close()
            elif (clue == "2"):
                print("flush clue1")
                ff = open("./levels/"+task+"/clue_1",'w')
                ff.write(acc)
                ff.close()
            elif (clue == "3"):
                print("flush clue2")
                ff = open("./levels/"+task+"/clue_2",'w')
                ff.write(acc)
                ff.close()
            acc = ""
        elif (not isComment):
            acc += line
        else:
            print("Comment: ", rcomment.group(0))

print("flush clue3")
ff = open("./levels/"+task+"/clue_3",'w')
ff.write(acc)
ff.close()
