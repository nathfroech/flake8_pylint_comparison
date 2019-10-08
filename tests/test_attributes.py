import pytest
from hamcrest import assert_that, contains_inanyorder, empty, is_

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

callable_check_params = [
    # code, flake8 rules, pylint rules
    param_wrapper("hasattr(o, '__call__')", {'B004', 'WPS421'}, set(), id='hasattr'),
    param_wrapper("getattr(o, '__call__', default=False)", {'B004', 'B009'}, set(), id='getattr'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', callable_check_params)
def test_detects_incorrect_check_for_callable(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(found_flake8_errors, contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(found_pylint_errors, contains_inanyorder(*pylint_errors))


def test_detects_using_getattr_with_hardcoded_name_and_without_default(file_to_lint):
    content = "getattr('abc', 'strip')\n"
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(found_flake8_errors, contains_inanyorder('B009'))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(found_pylint_errors, is_(empty()))


def test_detects_using_setattr_with_hardcoded_name(file_to_lint):
    content = "setattr(foo, 'bar', None)\n"
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(found_flake8_errors, contains_inanyorder('B010'))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(found_pylint_errors, is_(empty()))
