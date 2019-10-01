import pytest
from hamcrest import assert_that

from tests.linter_runners import violates_rules

A001 = {'A001'}
A002 = {'A002'}
A003 = {'A003'}

W0622 = {'W0622'}

params = [
    # code, flake8 rules, pylint rules
    pytest.param('max = 4', A001, W0622, id='top_level'),
    pytest.param((
        'def bla():\n'
        '    filter = 4'
    ), A001, W0622, id='variable_inside_function'),
    pytest.param((
        'class Bla:\n'
        '    def method(self):\n'
        '        int = 4'
    ), A001, W0622, id='var_inside_method'),
    pytest.param('bla, *int = range(4)', A001, W0622, id='starred_assignment'),
    pytest.param('[bla, int] = range(2)', A001, W0622, id='list_assignment'),
    pytest.param((
        'for format in (1, 2, 3):\n'
        '    continue'
    ), A001, W0622, id='for_loop'),
    pytest.param((
        'for index, format in enumerate([1,2,3]):\n'
        '    continue'
    ), A001, W0622, id='for_loop_multiple_variables'),
    pytest.param((
        'for [index, format] in enumerate([1,2,3]):\n'
        '    continue'
    ), A001, W0622, id='for_loop_multiple_variables_list'),
    pytest.param((
        'for index, (format, list) in enumerate([(1, "a"), (2, "b")]):\n'
        '    continue'
    ), A001, W0622, id='for_loop_nested'),
    pytest.param((
        'for index, *int in enumerate([(1, "a"), (2, "b")]):\n'
        '    continue'
    ), A001, W0622, id='for_loop_starred'),
    pytest.param((
        'with open("bla.txt") as dir:\n'
        '    pass'
    ), A001, W0622, id='with_statement'),
    pytest.param((
        'with open("bla.txt") as dir, open("bla.txt") as int:\n'
        '    pass'
    ), A001, W0622, id='with_statement_multiple'),
    pytest.param((
        'with open("bla.txt") as (dir, bla):\n'
        '    pass'
    ), A001, W0622, id='with_statement_unpack'),
    pytest.param((
        'with open("bla.txt") as [dir, bla]:\n'
        '    pass'
    ), A001, W0622, id='with_statement_unpack_list'),
    pytest.param((
        'with open("bla.txt") as (bla, *int):\n'
        '    pass'
    ), A001, W0622, id='with_statement_unpack_star'),
    pytest.param(
        'import zope.component.getSite as int',
        A001, W0622, id='import_as',
    ),
    pytest.param(
        'from zope.component import getSite as int',
        A001, W0622, id='import_from_as',
    ),
    pytest.param((
        'class int:\n'
        '    pass'
    ), A001, W0622, id='class_name'),
    pytest.param((
        'def int():\n'
        '    pass'
    ), A001, W0622, id='function_name'),
    pytest.param((
        'async def int():\n'
        '    pass'
    ), A001, W0622, id='async_function_name'),

    pytest.param((
        'async def bla():\n'
        '    async for int in range(4):\n'
        '        pass'
    ), A001, W0622, id='async for'),
    pytest.param((
        'async def bla():\n'
        '    async with open("bla.txt") as int:\n'
        '        pass'
    ), A001, W0622, id='async with'),
    pytest.param('[int for int in range(3,9)]', A001, {}, id='list_comprehension'),
    pytest.param(
        '[(int, list) for int, list in enumerate(range(3,9))]',
        A001, {}, id='list_comprehension_multiple',
    ),
    pytest.param(
        '[(int, a) for [int, a] in enumerate(range(3,9))]',
        A001, {}, id='list_comprehension_multiple_as_list',
    ),
    pytest.param((
        'try:\n'
        '    a = 2\n'
        'except Exception as int:\n'
        '    print("ooops")'
    ), A001, {}, id='exception'),

    pytest.param((
        'def bla(list):\n'
        '    a = 4'
    ), A002, W0622, id='function_parameter'),
    pytest.param((
        'def bla(dict=3):\n'
        '    a = 4'
    ), A002, W0622, id='function_keyword_parameter'),

    pytest.param((
        'class Bla:\n'
        '    object = 4'
    ), A003, {}, id='class_attribute'),
    pytest.param((
        'class Bla:\n'
        '    def int():\n'
        '        pass'
    ), A003, {}, id='method_name'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_variable_shadowing(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors=flake8_errors, pylint_errors=pylint_errors))
