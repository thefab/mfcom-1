#!/usr/bin/env python3

import argparse
import sys
from mfutil.plugins import install_plugin, get_plugin_info, \
    MFUtilPluginAlreadyInstalled, MFUtilPluginCantInstall
from mfutil.cli import echo_running, echo_nok, echo_ok

DESCRIPTION = "install a plugin file"


def main():
    arg_parser = argparse.ArgumentParser(description=DESCRIPTION)
    arg_parser.add_argument("plugin_filepath", type=str,
                            help="plugin filepath")
    args = arg_parser.parse_args()
    echo_running("- Checking plugin file...")
    infos = get_plugin_info(args.plugin_filepath, mode="file")
    if not infos:
        echo_nok()
        sys.exit(1)
    echo_ok()
    name = infos['metadatas']['name']
    echo_running("- Installing plugin %s..." % name)
    try:
        install_plugin(args.plugin_filepath)
    except MFUtilPluginAlreadyInstalled as e:
        echo_nok("already installed")
        sys.exit(1)
    except MFUtilPluginCantInstall as e:
        echo_nok()
        print(e)
        sys.exit(2)
    echo_ok()


if __name__ == '__main__':
    main()
