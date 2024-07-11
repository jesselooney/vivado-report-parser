import json
from pathlib import Path

from vivado_report_parser import parse_tables_report
from vivado_report_parser.timing import parse_data_path_delay

FIXTURES_DIR = Path(__file__).parent / 'fixtures'


def test_utilization():
    with open(FIXTURES_DIR / 'utilization.rpt', 'r') as f:
        report_str = f.read()

    report_data = parse_tables_report(report_str)
    report_json = json.dumps(report_data)

    with open(FIXTURES_DIR / 'utilization.json', 'r') as f:
        expected_report_json = f.read()

    assert(report_json == expected_report_json)


def test_data_path_delay():
    with open(FIXTURES_DIR / 'timing.rpt', 'r') as f:
        report_str = f.read()

    delay = parse_data_path_delay(report_str)

    assert(delay['total_ns'] == '3.005')
    assert(delay['logic_ns'] == '1.059')
    assert(delay['route_ns'] == '1.946')
