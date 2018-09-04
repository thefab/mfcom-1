#!/usr/bin/env python3

import os
import psutil
import sys
import argparse

from mfutil import kill_process_and_children
from mflog import getLogger

LOG = getLogger('kill_remaining_processes')
USER = os.environ.get('MODULE_RUNTIME_USER', None)
MODULE = os.environ.get('MODULE', None)
MODULE_RUNTIME_HOME = os.environ.get('MODULE_RUNTIME_HOME', None)
MODULE_RUNTIME_HOME_TMP = MODULE_RUNTIME_HOME + "/tmp" if MODULE_RUNTIME_HOME \
    is not None else None
if USER is None:
    LOG.critical("can't read MODULE_RUNTIME_USER env var")
    sys.exit(1)
if MODULE is None:
    LOG.critical("can't read MODULE env var")
    sys.exit(1)
CURRENT_PROCESS = psutil.Process()


def is_same_family(child, proc):
    if child.pid == proc.pid:
        return True
    try:
        parent = child.parent()
    except Exception:
        return False
    if parent is None:
        return False
    return is_same_family(parent, proc)


def get_processes_to_kill():
    processes_to_kill = []
    for proc in psutil.process_iter():
        if proc.username() != USER:
            continue
        if is_same_family(CURRENT_PROCESS, proc):
            continue
        cwd = ""
        try:
            cwd = proc.cwd()
        except Exception:
            pass
        if not cwd.startswith(MODULE_RUNTIME_HOME_TMP):
            try:
                env = proc.environ()
            except psutil.Error:
                continue
            if 'MODULE' not in env:
                continue
            if env['MODULE'] != MODULE:
                continue
            if env.get('METWORK_KILL_REMAINING', 'NONE') == '1':
                processes_to_kill.append(proc)
                continue
            if env.get('METWORK_KILL_REMAINING', 'NONE') == '0':
                continue
        if proc.terminal() is not None:
            continue
        processes_to_kill.append(proc)
    return processes_to_kill


argparser = argparse.ArgumentParser(description="kill remaining non-terminal "
                                    "processes after a module stop")
silent_doc = "silent mode: return only the number of processes killed and " \
    "the number of remaining processes"
argparser.add_argument("--silent", action="store_true", help=silent_doc)
args = argparser.parse_args()
processes_to_kill = get_processes_to_kill()
first_count = len(processes_to_kill)
for proc in processes_to_kill:
    if not args.silent:
        try:
            LOG.info("killing remaining process (and children): "
                     "pid:%i, cmdline: %s" % (proc.pid,
                                              " ".join(proc.cmdline())))
        except Exception:
            # we can have some exceptions here is some edge cases
            pass
    kill_process_and_children(proc.pid)

processes_to_kill = get_processes_to_kill()
second_count = len(processes_to_kill)
for proc in processes_to_kill:
    if not args.silent:
        try:
            LOG.warning("remaining process not killed: "
                        "pid:%i, cmdline: %s" % (proc.pid,
                                                 " ".join(proc.cmdline())))
        except Exception:
            # we can have some exceptions here is some edge cases
            pass

if args.silent:
    print("%i,%i" % (first_count, second_count))
if len(processes_to_kill) > 0:
    sys.exit(1)
sys.exit(0)
