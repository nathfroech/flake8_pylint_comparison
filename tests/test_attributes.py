import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

B004 = {'B004'}

callable_check_params = [
    # code, flake8 rules, pylint rules
    pytest.param('hasattr(o, "__call__")', B004, {}, id='hasattr'),
    pytest.param('getattr(o, "__call__", False)', B004, {}, id='getattr'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', callable_check_params)
def test_detects_incorrect_check_for_callable(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
