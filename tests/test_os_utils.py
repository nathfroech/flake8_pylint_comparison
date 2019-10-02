from hamcrest import assert_that

from tests.linter_runners import violates_rules


def test_detects_os_environ_assignment(file_to_lint):
    content = (
        'import os\n\n'  # noqa: P103 it's an empty dict, not string formatting
        'os.environ = {}'
    )

    file_to_lint.write_text(content)

    assert_that(file_to_lint, violates_rules(flake8_errors={'B003'}, pylint_errors={}))
