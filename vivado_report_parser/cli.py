import sys

from .utilization import parse_utilization_report


def run():
    if len(sys.argv) < 2:
        print(f'''
Please provide a utilization report file to parse.
Usage: {sys.argv[0]} <input_file> [<output_file>]
''')
        sys.exit(1)
    
    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        report = parse_utilization_report(f.read())

    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
        json.dump(report, output_file)
    else:
        print(json.dumps(report))
