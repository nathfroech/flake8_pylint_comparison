import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

params = [
    # code, flake8 rules, pylint rules
    param_wrapper((
        'def check_parameter(parameter_value=[1, 2, 3]):',
        '    return parameter_value',
    ), {'B006', 'WPS404'}, {'W0102'}, id='list_as_default'),
    param_wrapper((
        'def check_parameter(*, parameter_value=[1, 2, 3]):',
        '    return parameter_value',
    ), {'B006'}, set(), id='list_as_kwonly_default'),
    param_wrapper((
        'def check_parameter(parameter_value={}):',  # noqa: P103 it's an empty dict, not string formatting
        '    return parameter_value',
    ), {'B006', 'WPS404'}, {'W0102'}, id='dict_as_default'),
    param_wrapper((
        'def check_parameter(parameter_value=set()):',
        '    return parameter_value',
    ), {'B006', 'WPS404'}, {'W0102'}, id='set_as_default'),
    param_wrapper((
        'default_value = {1, 2, 3}',
        '',
        '',
        'def check_parameter(parameter_value=default_value):',
        '    return parameter_value',
    ), set(), {'W0102'}, id='variable_as_default'),
    param_wrapper((
        'import collections',
        '',
        '',
        'def check_parameter(parameter_value=collections.OrderedDict()):',
        '    return parameter_value',
    ), {'B006', 'WPS404'}, set(), id='ordered_dict_as_default'),
    param_wrapper((
        'import collections',
        '',
        '',
        'async def check_parameter(parameter_value=collections.OrderedDict()):',
        '    return parameter_value',
    ), {'B006', 'WPS404'}, set(), id='ordered_dict_as_async_default'),
    param_wrapper((
        'import time',
        '',
        '',
        'def check_parameter(parameter_value=time.time()):',
        '    return parameter_value',
    ), {'B008', 'WPS404'}, set(), id='call_as_default'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_incorrect_defaults_for_parameters(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder(*pylint_errors))
