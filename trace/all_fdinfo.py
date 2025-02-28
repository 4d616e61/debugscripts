import utils
import sys
import os




def main():
    
    if len(sys.argv) < 2:
        return
    pids = utils.pgrep(sys.argv[1])
    for pid in pids:
        print(f"PID: {pid}")
        for info in utils.get_all_fdinfo(pid):
            print(utils.fmt_fdinfo(info))



main()
