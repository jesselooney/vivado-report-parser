'''This module provides a function for parsing an arbitrary Vivado report as well as a CLI.'''

import json
import sys

import argparse

from vivado_report_parser.helpers import get_parser


def parse_vivado_report(report_text: str) -> dict | None:
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
        with open(args.file, 'r') as f:
            report_text = f.read()
    else:
        report_text = sys.stdin.read()

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
    
