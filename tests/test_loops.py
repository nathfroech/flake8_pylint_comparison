import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

params = [
    # code, flake8 rules, pylint rules
    pytest.param((
        'for i in range(10):\n'
        '    print(10)'
    ), {'B007'}, {}, id='simple_loop'),
    pytest.param((
        'for i in range(10):\n'
        '    for j in range(10):\n'
        '        for k in range(10):\n'
        '            print(i + j)'
    ), {'B007'}, {}, id='nested_loop'),
    pytest.param((
        'def strange_generator():\n'
        '    for i in range(10):\n'
        '        for j in range(10):\n'
        '            for k in range(10):\n'
        '                for l in range(10):\n'
        '                    yield i, (j, (k, l))\n\n\n'
        'for i, (j, (k, l)) in strange_generator():\n'
        '    print(j, l)'
    ), {'B007'}, {}, id='unpacking'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_unused_loop_variables(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
