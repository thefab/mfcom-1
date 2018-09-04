#!/usr/bin/env python3

import argparse
import sys
from mfutil.plugins import get_plugin_info

DESCRIPTION = "get some information about a plugin"


def main():
    arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
    arg_parser.add_argument("name_or_filepath", type=str,
                            help="installed plugin name (without version) or "
                            "full plugin filepath")
    args = arg_parser.parse_args()

    infos = get_plugin_info(args.name_or_filepath)
    if infos is None:
        sys.exit(1)

    print("Metadata:")
    print()
    print(infos['raw_metadata_output'])
    print()
    print("List of files:")
    print()
    print(infos['raw_files_output'])


if __name__ == '__main__':
    main()
