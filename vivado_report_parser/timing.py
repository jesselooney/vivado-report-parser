import re


# def parse_timing_report(report_str: str):
#     # First parse at a high level, e.g. summary at top, table
#     # Then take a second pass parsing the string values of these fields
#     # into more structured data
#     match = re.search('Timing Report\n\n(?P<summary>[.\n]+)\n')
#     summary = match.group('summary')

#     lines = summary.split('\n')
#     # Split at only the first ':' in the line
#     entries = [line.split(':', 1) for line in lines]
#     # Some lines in this report "wrap over" with a newline. We can find
#     # them by searching for entries that have not been split into


def parse_data_path_delay(report_str: str):
    num = r'\d+\.?\d*'
    match = re.search(rf'Data Path Delay:\s*({num})ns.*logic ({num})ns.*route ({num})ns', report_str)
    return {
        'total_ns': match.group(1),
        'logic_ns': match.group(2),
        'route_ns': match.group(3)
    }
    
    
