import os
import sys
import subprocess
import utils

def main():
    if len(sys.argv) < 2:
        return
    pids = utils.pgrep(sys.argv[1])
    for pid in pids:
        print(f"PID: {pid}")
        threads = os.listdir(f"/proc/{pid}/task")
        for t in threads:
            print(f"TID: {t}")
            s = utils.get_stack(t)
            print(s)
main()
