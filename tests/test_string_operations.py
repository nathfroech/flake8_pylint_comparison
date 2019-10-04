import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

strip_params = [
    # code, flake8 rules, pylint rules
    param_wrapper("s.strip('abca')", {'B005'}, set(), id='strip_string'),
    param_wrapper(r"s.strip(r'\n\t ')", {'B005'}, set(), id='strip_raw_string'),
    param_wrapper("s.lstrip('abca')", {'B005'}, set(), id='lstrip_string'),
    param_wrapper(r"s.lstrip(r'\n\t ')", {'B005'}, set(), id='lstrip_raw_string'),
    param_wrapper("s.rstrip('abca')", {'B005'}, set(), id='rstrip_string'),
    param_wrapper(r"s.rstrip(r'\n\t ')", {'B005'}, set(), id='rstrip_raw_string'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', strip_params)
def test_detects_strip_with_multicharacter_string(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder(*pylint_errors))
