"""Encrypt file for DIDWW API 3

usage: didww_encrypt [-h] [-i [INPUT]] [-o [OUTPUT]] [-f] (-m [{sandbox,production}] | -u [URI])

Encrypt file for DIDWW API 3

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        use input pipe when not passed
  -o [OUTPUT], --output [OUTPUT]
                        use output pipe when not passed
  -f, --fingerprint     return fingerprint for public keys
  -m [{sandbox,production}], --mode [{sandbox,production}]
                        which DIDWW server use for public keys fetching
  -u [URI], --uri [URI]
                        custom URI for public keys fetching
"""

import os
import sys
import argparse
import io
import urllib
from . import Encrypt, MODES


def main(prog="didww_encrypt", args=None):
    parser = argparse.ArgumentParser(prog=prog, description=__doc__)
    parser.add_argument(
        "-i",
        "--input",
        nargs="?",
        dest="input",
        type=argparse.FileType("rb"),
        help="use input pipe when not passed",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        dest="output",
        type=argparse.FileType("wb"),
        help="use output pipe when not passed",
        default=sys.stdout.buffer,
    )
    parser.add_argument(
        "-f",
        "--fingerprint",
        action="store_true",
        dest="fingerprint",
        help="return fingerprint for public keys",
        default=False,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-m",
        "--mode",
        nargs="?",
        dest="mode",
        type=str,
        choices=MODES,
        help="which DIDWW server use for public keys fetching",
    )
    group.add_argument(
        "-u",
        "--uri",
        nargs="?",
        dest="uri",
        type=str,
        help="custom URI for public keys fetching",
    )
    options = parser.parse_args(args)
    # if no fingerprint option and no input option and stdin connected to pipeline
    # then use stdin as input
    if not options.fingerprint and options.input is None:
        if sys.stdin.isatty():
            sys.stderr.write("input file or pipe data must be provided\n")
            return 2
        else:
            options.input = sys.stdin.buffer

    try:
        __process_command_line(options)
        return 0
    except urllib.error.HTTPError as error:
        sys.stderr.write(
            f"failed to fetch keys from {error.url}: {error.code} {error.msg}\n"
        )
        return 3

    finally:
        if isinstance(options.input, io.BufferedReader):
            options.input.close()
        if isinstance(options.output, io.BufferedWriter):
            options.output.close()


def __process_command_line(options):
    encryptor = Encrypt.new(mode=options.mode, uri=options.uri)
    if options.fingerprint:
        result = (encryptor.fingerprint + os.linesep).encode("ascii")
    else:
        result = encryptor.encrypt(options.input.read())
    options.output.write(result)
