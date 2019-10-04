import pytest
from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import param_wrapper, run_flake8, run_pylint

params = [
    # code, flake8 rules, pylint rules
    param_wrapper((
        'values = []',
        'for i in range(10):',
        '    values.append(10)',
    ), {'B007'}, set(), id='simple_loop'),
    param_wrapper((
        'values = []',
        'for i in range(10):',
        '    for j in range(10):',
        '        for k in range(10):',
        '            values.append(i + j)',
    ), {'B007'}, set(), id='nested_loop'),
    param_wrapper((
        'def strange_generator():',
        '    for x in range(10):',
        '        for y in range(10):',
        '            for z in range(10):',
        '                for w in range(10):',
        '                    yield x, (y, (z, w))',
        '',
        '',
        'values = []',
        'for i, (j, (k, l)) in strange_generator():',
        '    values.append(j, l)',
    ), {'B007', 'WPS405', 'WPS414'}, set(), id='unpacking'),
]


@pytest.mark.parametrize('content,flake8_errors,pylint_errors', params)
def test_detects_unused_loop_variables(content, flake8_errors, pylint_errors, file_to_lint):
    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder(*flake8_errors))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder(*pylint_errors))
