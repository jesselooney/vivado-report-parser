import json
from pathlib import Path
import pickle

from vivado_report_parser import parse_vivado_report

FIXTURES_DIR = Path(__file__).parent / 'fixtures'
INPUTS_DIR = FIXTURES_DIR / 'inputs'
OUTPUTS_DIR = FIXTURES_DIR / 'outputs'
GOLDENS_DIR = FIXTURES_DIR / 'goldens'


def pytest_generate_tests(metafunc):
    input_files = list(INPUTS_DIR.iterdir())
    output_files = [OUTPUTS_DIR / file.name for file in input_files]
    golden_files = [GOLDENS_DIR / file.name for file in input_files]
    metafunc.parametrize('input_file, output_file, golden_file',
                         zip(input_files, output_files, golden_files))


def test_input(input_file, output_file, golden_file, should_update_goldens):
    with input_file.open('r', newline='') as f:
        file_content = f.read()

    report = parse_vivado_report(file_content)

    with output_file.open('w', newline='') as f:
        json.dump(report, f)

    if should_update_goldens:
        with golden_file.open('wb') as f:
            pickle.dump(report, f)

    with golden_file.open('rb') as f:
        golden_report = pickle.load(f)

    assert report == golden_report
