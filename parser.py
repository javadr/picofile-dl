#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configargparse as argparse
import sys
import tempfile
import info


def parse_args(args=None):
    """
    Parse the arguments/options passed to the program on the command line.
    """

    parse_kwargs = {
        "description": 'Download a file/bunch of files from picofile server.'
    }
    parser = argparse.ArgParser(**parse_kwargs)

    # Basic options
    group_basic = parser.add_argument_group('Basic options')

    group_basic.add_argument(
        '-u',
        '--url',
        dest='url',
        action='store',
        default=None,
        help='a specific url that you want to download from picofile')

    group_basic.add_argument('-f',
                             '--filename',
                             dest='filename',
                             action='store',
                             default=None,
                             help='a file includes the picofile urls')

    group_basic.add_argument(
        '-p',
        '--path',
        dest='path',
        action='store',
        default=f"{tempfile.gettempdir()}/picofile-dl",
        help='path to save dowloaded files (Default: /<TEMP>/picofile-dl)')

    parser.add_argument('-v',
                        '--version',
                        dest='version',
                        action='store_true',
                        default=False,
                        help='display version and exit')

    parser.add_argument('--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='display more info')

    # Final parsing of the options
    args = parser.parse_args(args)

    # show version?
    if args.version:
        print(
            f"Picofile-dl Ver. {info.__version__}, released on {info.__date__}"
        )
        sys.exit(0)

    if not ((args.url and not args.filename) or (not args.url and args.filename)):
        parser.print_usage()
        sys.exit(1)

    return args
