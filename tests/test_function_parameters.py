import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

B006 = {'B006'}

W0102 = {'W0102'}

params = [
    # code, flake8 rules, pylint rules
    pytest.param((
        'def foo(value=[1, 2, 3]):\n'
        '    pass'
    ), B006, W0102, id='list_as_default'),
    pytest.param((
        'def foo(*, value=[1, 2, 3]):\n'
        '    pass'
    ), B006, {}, id='list_as_kwonly_default'),
    pytest.param((
        'def foo(value={}):\n'  # noqa: P103 it's an empty dict, not string formatting
        '    pass'
    ), B006, W0102, id='dict_as_default'),
    pytest.param((
        'def foo(value=set()):\n'
        '    pass'
    ), B006, W0102, id='set_as_default'),
    pytest.param((
        'DEFAULT = {1, 2, 3}\n\n'
        'def foo(value=DEFAULT):\n'
        '    pass'
    ), {}, W0102, id='variable_as_default'),
    pytest.param((
        'import collections\n\n\n'
        'def foo(value=collections.OrderedDict()):\n'
        '    pass'
    ), B006, {}, id='ordered_dict_as_default'),
    pytest.param((
        'import collections\n\n\n'
        'async def foo(value=collections.OrderedDict()):\n'
        '    pass'
    ), B006, {}, id='ordered_dict_as_async_default'),
    pytest.param((
        'import time\n\n\n'
        'def foo(value=time.time()):\n'
        '    pass\n'
    ), {'B008'}, {}, id='call_as_default'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_incorrect_defaults_for_parameters(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
