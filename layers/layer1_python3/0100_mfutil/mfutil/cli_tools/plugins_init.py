#!/usr/bin/env python3

import argparse
import sys
from mfutil.plugins import init_plugins_base, is_plugins_base_initialized, \
    MFUtilPluginCantInit
from mfutil.cli import echo_ok, echo_running, echo_nok

DESCRIPTION = "init the plugins base (dangerous)"


def main():
    arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
    arg_parser.parse_args()
    echo_running("- Creating plugins base...")
    try:
        init_plugins_base()
    except MFUtilPluginCantInit as e:
        echo_nok()
        print(e)
        sys.exit(1)
    if not is_plugins_base_initialized():
        echo_nok()
        sys.exit(1)
    echo_ok()


if __name__ == '__main__':
    main()
