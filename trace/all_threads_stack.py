import os
import sys
import subprocess


def main():
    if len(sys.argv) < 2:
        return
    pids = subprocess.check_output(["pgrep", sys.argv[1]]).decode().split()
    for pid in pids:
        print(f"PID: {pid}")
        threads = os.listdir(f"/proc/{pid}/task")
        for t in threads:
            print(f"TID: {t}")
            with open(f"/proc/{t}/stack", "r") as f:
                print(f.read())


main()
