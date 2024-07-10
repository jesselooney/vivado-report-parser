import json
from pathlib import Path

from vivado_report_parser.utilization import parse_utilization_report

FIXTURES_DIR = Path(__file__).parent / 'fixtures'

def test_utilization():
    with open(FIXTURES_DIR / 'utilization.rpt', 'r') as f:
        report_str = f.read()

    report_data = parse_utilization_report(report_str)
    report_json = json.dumps(report_data)

    with open(FIXTURES_DIR / 'utilization.json', 'r') as f:
        expected_report_json = f.read()

    assert(report_json == expected_report_json)

