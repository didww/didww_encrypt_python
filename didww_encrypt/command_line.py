import os
import sys
import select
import argparse
from . import Encrypt


def input_has_data(infile):
    return select.select([infile, ], [], [], 0.0)[0]


def main(prog="didww_encrypt"):
    description = "Encrypt file for DIDWW API 3"
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        "-i", "--input",
        nargs="?",
        type=argparse.FileType("rb"),
        help="use input pipe when not passed",
        default=sys.stdin.buffer
    )
    parser.add_argument(
        "-o", "--output",
        nargs="?",
        type=argparse.FileType("wb"),
        help="use output pipe when not passed",
        default=sys.stdout.buffer
    )
    parser.add_argument(
        "-f", "--fingerprint",
        action="store_true",
        dest="fingerprint",
        help="return fingerprint for public keys",
        default=False
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-m", "--mode",
        nargs="?",
        dest="mode",
        type=str,
        choices=Encrypt.MODES,
        help="which DIDWW server use for public keys fetching"
    )
    group.add_argument(
        "-u", "--uri",
        nargs="?",
        dest="uri",
        type=str,
        help="custom URI for public keys fetching"
    )
    options = parser.parse_args()
    encryptor = Encrypt.new(mode=options.mode, uri=options.uri)
    if options.fingerprint:
        result = (encryptor.fingerprint + os.linesep).encode('ascii')
    else:
        if not input_has_data(options.input):
            sys.stderr.write("input file or pipe data must be provided\n")
            exit(2)
        result = encryptor.encrypt(options.input.read())
    options.output.write(result)
    return 0
