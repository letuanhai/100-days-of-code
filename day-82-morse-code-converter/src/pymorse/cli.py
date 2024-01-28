import argparse
import sys
from typing import Optional, Sequence

from pymorse.morse import encode
from pymorse import __version__


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pymorse",
        description="A Python CLI app to convert text to morse code.",
        epilog="Thanks for using %(prog)s!",
    )
    parser.add_argument("message", help="The message to convert")
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )

    args = parser.parse_args(argv)  # if argv==None it will parse sys.argv
    return args


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    try:
        print(encode(args.message))
    except ValueError as e:
        # parser.exit(status=100, message=e.args[0])
        # Use custom exit code instead of Argument parser built-in to separate responsibility
        sys.stderr.write(e.args[0])
        sys.exit(100)
