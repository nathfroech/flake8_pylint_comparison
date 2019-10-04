from hamcrest import assert_that, contains_inanyorder

from tests.testing_utils import run_flake8, run_pylint


def test_detects_os_environ_assignment(file_to_lint):
    content = (
        'import os\n\n'  # noqa: P103 it's an empty dict, not string formatting
        'os.environ = {}\n'
    )

    file_to_lint.write_text(content)

    found_flake8_errors = run_flake8(file_to_lint)
    assert_that(set(found_flake8_errors), contains_inanyorder('B003'))

    found_pylint_errors = run_pylint(file_to_lint)
    assert_that(set(found_pylint_errors), contains_inanyorder())
