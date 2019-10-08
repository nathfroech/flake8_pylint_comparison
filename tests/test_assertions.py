import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

false_assert_params = [
    # code, flake8 rules, pylint rules
    param_wrapper('assert False', {'B011', 'S101', 'WPS444'}, set(), id='without_message'),
    param_wrapper("assert False, 'message'", {'B011', 'S101', 'WPS444'}, set(), id='with_message'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', false_assert_params)
def test_detects_assert_false(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(found_flake8_errors, contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(found_pylint_errors, contains_inanyorder(*pylint_errors))
