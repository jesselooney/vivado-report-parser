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

    try:
        result = parse_vivado_report(file_content)
        with output_file.open('w', newline='') as f:
            json.dump(result, f)
    except NotImplementedError as e:
        result = e
        with output_file.open('w', newline='') as f:
            f.write(repr(result))

    if should_update_goldens:
        with golden_file.open('wb') as f:
            pickle.dump(result, f)

    with golden_file.open('rb') as f:
        golden_result = pickle.load(f)

    if isinstance(golden_result, NotImplementedError):
        assert isinstance(result, NotImplementedError)
        assert result.args == golden_result.args
    else:
        assert result == golden_result
