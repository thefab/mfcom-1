#!/usr/bin/env python3

import argparse
from mfutil.plugins import get_installed_plugins

DESCRIPTION = "get the installed plugins list"


def main():
    arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
    arg_parser.add_argument("--raw", action="store_true", help="raw mode")
    args = arg_parser.parse_args()
    plugins = get_installed_plugins()
    if not args.raw:
        print("Installed plugins:")
        print()
        print("| %-25s | %-25s | %.25s" % ("NAME", "VERSION", "RELEASE"))
        print("-" * 75)
    for plugin in plugins:
        name = plugin['name']
        release = plugin['release']
        version = plugin['version']
        if args.raw:
            print("%s~~~%s~~~%s" % (name, version, release))
        else:
            print("| %-25s | %-25s | %.25s" % (name, version, release))
    if not args.raw:
        print()
        print("Total: %i plugin(s)" % len(plugins))


if __name__ == '__main__':
    main()
