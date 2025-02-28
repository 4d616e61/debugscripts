import os
import subprocess


_G_os_fd_flags = None


def pgrep(name : str) -> list:
    return subprocess.check_output(["pgrep", name]).decode().split()



def list_proc_info(pid, info) -> list:
    return os.listdir(f"/proc/{pid}/{info}")


def list_tid(pid) -> list:
    return list_proc_info(pid, "task")

def list_fdinfo(pid) -> list:
    return list_proc_info(pid, "fdinfo")


def get_stack(tid):
    with open(f"/proc/{tid}/stack", "r") as f:
        r = f.read()
    return r

def get_fdinfo(pid, fd):
    with open(f"/proc/{pid}/fdinfo/{fd}", "r") as f:
        r = f.read()
    l = os.readlink(f"/proc/{pid}/fd/{fd}")
    res = {}
    for line in r.split("\n"):
        if len(line) == 0:
            continue
        k = line.split(":")[0]
        v = line.split(":")[1].lstrip("\t")
        res[k] = v
    res['fname'] = l
    return res


def fmt_fdinfo(fdinfo) -> str:
    flags_list = ""
    for k, v in get_fd_flags().items():
        if not test_flags(int(fdinfo["flags"]), v):
            continue
        flags_list += k + " "
    return f"""Filename: {fdinfo["fname"]}
    Flags: {flags_list}
    """


def get_all_fdinfo(pid):
    res = []
    for fd in list_fdinfo(pid):
        try:
            res.append(get_fdinfo(pid, fd))
        except FileNotFoundError:
            pass
    return res


def get_fd_flags():
    global _G_os_fd_flags
    if _G_os_fd_flags != None:
        return _G_os_fd_flags
    os_dir = dir(os)
    res = {}
    for v in os_dir:
        if not v.startswith("O_"):
            continue
        res[v] = os.__dict__[v]
    _G_os_fd_flags = res
    return res


def test_flags(flags, target) -> bool:
    return target & flags == target

