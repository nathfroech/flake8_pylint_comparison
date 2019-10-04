import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

unary_operator_params = [
    # code, flake8 rules, pylint rules
    param_wrapper('x = ++1', {'B002', 'WPS330'}, {'E0107'}, id='assigning_plus_plus'),
    param_wrapper('++1', {'B002', 'WPS330'}, {'E0107'}, id='inplace_plus_plus'),
    param_wrapper('x = (++2) * 3', {'B002', 'WPS330'}, {'E0107'}, id='expression_part_plus_plus'),
    param_wrapper('x = --1', {'WPS330'}, {'E0107'}, id='assigning_minus_minus'),
    param_wrapper('--1', {'WPS330'}, {'E0107'}, id='inplace_minus_minus'),
    param_wrapper('x = (--2) * 3', {'WPS330'}, {'E0107'}, id='expression_part_minus_minus'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', unary_operator_params)
def test_detects_unnecessary_unary_operators(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(found_flake8_errors, contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(found_pylint_errors, contains_inanyorder(*pylint_errors))
