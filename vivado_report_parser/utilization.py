import json
import re
import sys


def _parse_utilization_table(table_str: str):
    # Expects a string starting and ending with '+' that contains a table
    # in the Vivado utilization report format.

    lines = table_str.split('\n')
    # Remove the three lines containing table dividers and borders (only two
    # lines if the table has no non-header rows).
    if len(lines) > 3:
        del lines[-1]
    del lines[2]
    del lines[0]

    # Parse the remaining lines so that rows becomes a 2D list
    # containing every cell in the table.
    rows = []
    for line in lines:
        fields = line.strip(' |').split('|')
        rows.append([field.strip() for field in fields])

    # Convert from the nested array format of `rows` to a JSON-like
    # list of dictionaries associating, for each row, the column names
    # with the corresponding values in those columns.
    table_header = rows[0]
    return [dict(zip(table_header, row)) for row in rows[1:]]

def parse_utilization_report(report_str: str):
    # This kind of report has multiple sections with headers of the form
    #
    #     <section_number> <section_title>
    #     --------------------------------
    #
    # where section_number is a string beginning with a decimal digit and
    # containing only decimal digits and periods. Each section contains a
    # table of the form
    #
    #     +-----------+-----------+-----+
    #     | col1_name | col2_name | ... |
    #     +-----------+-----------+-----+
    #     | col1_val1 | col2_val2 | ... |
    #     | col2_val2 | col2_val2 | ... |
    #     | ...       | ...       | ... |
    #     +-----------+-----------+-----+
    # 
    # Therefore, the top-level regex matches strings that start with a section
    # header and captures the section_title and all the contiguous following lines
    # that start with either '+' or '|' (i.e. the lines that make up the table).
    
    matches = re.findall(r'\d[\d\.]* (.+)\s-+\s\s((?:[+|].*\s)+)', report_str)

    report = {}
    for match in matches:
        section_title = match[0].strip()
        section_table = _parse_utilization_table(match[1].strip())
        report[section_title] = section_table

    # TODO: Parse Table of Contents and check it against the keys of `report`.

    return report


def main():
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


if __name__ == '__main__':
    main()
