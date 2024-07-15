import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--update-goldens",
        action="store_true",
        help="regenerate the golden test files for all tests that use them",
    )


@pytest.fixture
def should_update_goldens(request):
    return request.config.getoption("--update-goldens")
