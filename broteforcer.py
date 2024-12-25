#!/usr/bin/python

import requests
from threading import Thread
import sys
import getopt

def banner ():
    print(f"#########################")
    print(f"* Our Basic Bruteforcer *")
    print(f"#########################")

def start(argv):
    banner()
    try:
        opts, args = getopt.getopt(argv, "u:w:f:t")
    except getopt.GetoptError:
        print(f"Error on arguements")
        sys.exit()
    for opt,arg in opts:
        if opt == '-u':
            user = arg
        elif opt == '-w':
            url = arg
        elif opt == '-f':
            passlist = arg
        elif opt == '-t':
            threads = arg
    try:
        f = open(passlist, "r")
        passwords = f.readlines()
    except:
        print(f"[!!]Cant open that file")
        sys.exit()
    launcher_thread(passwords, threads, user, url):
    



if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print(f"[!!]Interrupted")