import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

params = [
    # code, flake8 rules, pylint rules
    param_wrapper((
        'try:',
        '    some_value = 1 / 0',
        'except:',
        '    some_value = 0',
    ), {'B001', 'E722', 'WPS344'}, {'W0702'}, id='bare_except'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_exception_catching_problems(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder(*pylint_errors))
