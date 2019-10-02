import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

B001 = {'B001'}

W0702 = {'W0702'}

params = [
    # code, flake8 rules, pylint rules
    pytest.param((
        'try:\n'
        '    import something\n'
        'except:\n'
        '    # should be except ImportError:\n'
        '    import something_else as something'
    ), B001, W0702, id='bare_except'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_exception_catching_problems(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
