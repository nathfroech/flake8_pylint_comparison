import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

B005 = {'B005'}

strip_params = [
    # code, flake8 rules, pylint rules
    pytest.param('s.strip("abca")', B005, {}, id='strip_string'),
    pytest.param(r's.strip(r"\n\t ")', B005, {}, id='strip_raw_string'),
    pytest.param('s.lstrip("abca")', B005, {}, id='lstrip_string'),
    pytest.param(r's.lstrip(r"\n\t ")', B005, {}, id='lstrip_raw_string'),
    pytest.param('s.rstrip("abca")', B005, {}, id='rstrip_string'),
    pytest.param(r's.rstrip(r"\n\t ")', B005, {}, id='rstrip_raw_string'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', strip_params)
def test_detects_strip_with_multicharacter_string(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
