'''This module provides a function for parsing an arbitrary Vivado report as well as a CLI.'''

import json
import sys

import argparse

from vivado_report_parser.helpers import get_parser


def parse_vivado_report(report_text: str) -> dict | None:
    '''Parses a Vivado report file as a dict.

    Reads the text content of a Vivado report file and selects the appropriate
    parser from this library. If no parser is available, returns None.
    Otherwise, returns the result of applying the parser to the report_text.

    Args:
        report_text: The text content of a Vivado report file to parse.
    Returns:
        A dict containing the parsed report according to the specifications of
        the parser used, or None if no parser is available.
    '''
    parse_report = get_parser(report_text)
    if parse_report is None:
        return None
    else:
        return parse_report(report_text)


def main():
    parser = argparse.ArgumentParser(description='Parse Vivado report files.')
    parser.add_argument('file', nargs='?', help='Vivado report file to parse')
    parser.add_argument('-d', '--dest', help='file to which output should be written')
    
    args = parser.parse_args()

    if args.file is not None:
        try:
            # Read file without converting \r\n to \n
            with open(args.file, 'r', newline='') as f:
                report_text = f.read()
        except (FileNotFoundError, IsADirectoryError) as e:
            print(e)
            sys.exit(e.errno)
    else:
        try:
            report_text = sys.stdin.read()
        except KeyboardInterrupt as e:
            print(e)
            sys.exit(130) # See https://tldp.org/LDP/abs/html/exitcodes.html.

    report = parse_vivado_report(report_text)

    if report is None:
        print('Error: This type of report file is not currently supported.')
        sys.exit(1)

    output = json.dumps(report)

    if args.dest:
        with open(args.dest, 'w') as f:
            f.write(output)
    else:
        sys.stdout.write(output)
    
