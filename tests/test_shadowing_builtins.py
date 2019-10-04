import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

params = [
    # code, flake8 rules, pylint rules
    param_wrapper('max = 4', {'A001'}, {'W0622'}, id='top_level'),
    param_wrapper((
        'def bla():',
        '    filter = 4',
    ), {'A001'}, {'W0622'}, id='variable_inside_function'),
    param_wrapper((
        'class Bla:',
        '    def method(self):',
        '        int = 4',
    ), {'A001'}, {'W0622'}, id='var_inside_method'),
    param_wrapper('bla, *int = range(4)', {'A001'}, {'W0622'}, id='starred_assignment'),
    param_wrapper('[bla, int] = range(2)', {'A001'}, {'W0622'}, id='list_assignment'),
    param_wrapper((
        'for format in (1, 2, 3):',
        '    continue',
    ), {'A001', 'B007', 'WPS327', 'WPS328'}, {'W0622'}, id='for_loop'),
    param_wrapper((
        'for index, format in enumerate([1, 2, 3]):',
        '    continue',
    ), {'A001', 'B007', 'WPS327', 'WPS328'}, {'W0622'}, id='for_loop_multiple_variables'),
    param_wrapper((
        'for [index, format] in enumerate([1, 2, 3]):',
        '    continue',
    ), {'A001', 'B007', 'WPS327', 'WPS328', 'WPS405'}, {'W0622'}, id='for_loop_multiple_variables_list'),
    param_wrapper((
        "for index, (format, list) in enumerate([(1, 'a'), (2, 'b')]):",
        '    continue',
    ), {'A001', 'B007', 'WPS221', 'WPS327', 'WPS328', 'WPS405', 'WPS414'}, {'W0622'}, id='for_loop_nested'),
    param_wrapper((
        "for index, *int in enumerate([(1, 'a'), (2, 'b')]):",
        '    continue',
    ), {'A001', 'B007', 'WPS327', 'WPS328'}, {'W0622'}, id='for_loop_starred'),
    param_wrapper((
        "with open('bla.txt') as dir:",
        '    pass',
    ), {'A001', 'WPS328', 'WPS420'}, {'W0622'}, id='with_statement'),
    param_wrapper((
        "with open('bla.txt') as dir, open('bla.txt') as int:",
        '    pass',
    ), {'A001', 'WPS316', 'WPS328', 'WPS420'}, {'W0622'}, id='with_statement_multiple'),
    param_wrapper((
        "with open('bla.txt') as (dir, bla):",
        '    pass',
    ), {'A001', 'WPS328', 'WPS420'}, {'W0622'}, id='with_statement_unpack'),
    param_wrapper((
        "with open('bla.txt') as [dir, bla]:",
        '    pass',
    ), {'A001', 'WPS328', 'WPS406', 'WPS420'}, {'W0622'}, id='with_statement_unpack_list'),
    param_wrapper((
        "with open('bla.txt') as (bla, *int):",
        '    pass',
    ), {'A001', 'WPS328', 'WPS420'}, {'W0622'}, id='with_statement_unpack_star'),
    param_wrapper(
        'import datetime as int',
        {'A001', 'F401'}, {'W0611', 'W0622'}, id='import_as',
    ),
    param_wrapper(
        'from datetime import datetime as int',
        {'A001', 'F401'}, {'W0611', 'W0622'}, id='import_from_as',
    ),
    param_wrapper((
        'class int:',
        '    pass',
    ), {'A001', 'N801', 'WPS420', 'WPS604'}, {'W0622'}, id='class_name'),
    param_wrapper((
        'def int():',
        '    return 1',
    ), {'A001'}, {'W0622'}, id='function_name'),
    param_wrapper((
        'async def int():',
        '    pass',
    ), {'A001', 'WPS420'}, {'W0622'}, id='async_function_name'),

    param_wrapper((
        'async def bla():',
        '    async for int in range(4):',
        '        pass',
    ), {'A001', 'WPS328', 'WPS420'}, {'E1133', 'W0622'}, id='async for'),
    param_wrapper((
        'async def bla():',
        "    async with open('bla.txt') as int:",
        '        pass',
    ), {'A001', 'WPS328', 'WPS420'}, {'W0622'}, id='async with'),
    param_wrapper('[int for int in range(3, 9)]', {'A001'}, {'R1721', 'W0106'}, id='list_comprehension'),
    param_wrapper(
        '[(int, list) for int, list in enumerate(range(3, 9))]',
        {'A001', 'WPS200'}, {'R1721', 'W0106'}, id='list_comprehension_multiple',
    ),
    param_wrapper(
        '[(int, a) for [int, a] in enumerate(range(3, 9))]',
        {'A001', 'WPS200', 'WPS405'}, {'W0106'}, id='list_comprehension_multiple_as_list',
    ),
    param_wrapper((
        'try:',
        '    a = 2',
        'except Exception as int:',
        '    a = 1',
    ), {'A001'}, {'W0703'}, id='exception'),

    param_wrapper((
        'def bla(list):',
        '    a = 4',
    ), {'A002'}, {'W0613', 'W0622'}, id='function_parameter'),
    param_wrapper((
        'def bla(dict=3):',
        '    a = 4',
    ), {'A002'}, {'W0613', 'W0622'}, id='function_keyword_parameter'),

    param_wrapper((
        'class Bla:',
        '    object = 4',
    ), {'A003'}, set(), id='class_attribute'),
    param_wrapper((
        'class Bla:',
        '    def int(self):',
        '        pass',
    ), {'A003', 'WPS420'}, set(), id='method_name'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_variable_shadowing(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder(*pylint_errors))
