import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

B002 = {'B002'}
WPS330 = {'WPS330'}

E0107 = {'E0107'}

unary_operator_params = [
    # code, flake8 rules, pylint rules
    pytest.param('x = ++1', B002, E0107, id='assigning_plus_plus'),
    pytest.param('++1', B002, E0107, id='inplace_plus_plus'),
    pytest.param('x = (++2) * 3', B002, E0107, id='expression_part_plus_plus'),
    pytest.param('x = --1', WPS330, E0107, id='assigning_minus_minus'),
    pytest.param('--1', WPS330, E0107, id='inplace_minus_minus'),
    pytest.param('x = (--2) * 3', WPS330, E0107, id='expression_part_minus_minus'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', unary_operator_params)
def test_detects_unnecessary_unary_operators(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
