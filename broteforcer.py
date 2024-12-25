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

if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print(f"Interrupted!!!")