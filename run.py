#! /usr/bin/env python
import sys
import subprocess


def Log():
    logno = input("logno: ")
    loghash = input("loghash: ")
    logname = input("logname: ")
    logorg = input("logorg: ")
    logdate = input("logdate (YYYY-MM-DD HH:MM:SS): ")

    subprocess.call("node trans_Log.js " + str(logno) + " " + str(loghash) + " " + str(logname) + " " + str(logorg) + " " + str(logdate), shell=True)

def LogImage():
    logno = input("logno: ")
    url = input("url: ")
    filehash = input("filehash: ")

    subprocess.call("node trans_LogImage.js " + str(logno) + " " + str(url) + " " + str(filehash), shell=True)

def LogSection():
    logno = input("logno: ")
    title = input("title: ")
    begin = input("begin: ")
    end = input("end: ")

    subprocess.call("node trans_LogSection.js " + str(logno) + " " + str(title) + " " + str(begin) + " " + str(end), shell=True)

def Query():
    qtype = int(input("query type (1:query from web 2: getPastEvents): "))
    logno = input("logno: ")

    if qtype == 2:
        event = input("event: ")
        fromB = input("from: ")
        toB = input("to: ")

        subprocess.call("node query.js " + str(event) + " " + str(logno) + " " + str(fromB) + " " + str(toB), shell=True)

    elif qtype == 1:
        subprocess.call("python3 query.py " + str(logno), shell=True)

if __name__=='__main__':

    while(1):
        #print("Enter command:\n1: 上鍊\n2: 查詢\n3: Exit\n: ")

        cmd = int(input("\nEnter command:\n1: 上鍊\n2: 查詢\n3: Exit\n: "))

        if cmd == 1:
            c = int(input("\t(1) FoodLog(uint256 logno, string loghash, string logname, string logorg, string logdate)\n\t(2) FoodLogImage(uint256 logno, string url, string filehash)\n\t(3) FoodLogSection(uint256 logno, string title, string begin, string end)\n\t: "))

            if c == 1:
                Log()
            elif c == 2:
                LogImage()
            elif c == 3:
                LogSection()
            
        elif cmd == 2:
            Query()
        elif cmd == 3:
            sys.exit()
        else:
            print('Wrong command!')


