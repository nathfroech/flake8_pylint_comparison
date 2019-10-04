import pathlib
import re
import subprocess
from typing import Iterable, List, Optional, Pattern, Sequence, Set, Union

import pytest
from _pytest.mark import ParameterSet  # noqa: WPS436 used for type check

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]

FLAKE8_ERROR_PATTERN = re.compile(r'(?P<module>/tmp/.+\.py):(?P<line>\d+): \[(?P<code>[A-Z]+\d+):?\] (?P<message>.+)')
PYLINT_ERROR_PATTERN = re.compile(r'(?P<module>/tmp/.+\.py):(?P<line>\d+):(?P<col>\d+): (?P<code>[A-Z]+\d+): (?P<message>.+) \((?P<verbose_code>[a-z\-]+)\)')  # noqa: E501 line too long


ErrorCodes = Optional[Iterable[str]]

# Rules that will be broken pretty often in code parts, used in tests
DEFAULT_FLAKE8_IGNORES = (
    'C101',  # Coding magic comment not found
    'D100',  # Missing docstring in public module
    'D101',  # Missing docstring in public class
    'D102',  # Missing docstring in public method
    'D103',  # Missing docstring in public function
    'F821',  # Undefined name
    'F841',  # Local variable is assigned to but never used
    'WPS110',  # Blacklisted name
    'WPS111',  # Name too short
    'WPS114',  # Underscored numbers pattern
    'WPS306',  # Found class without a base class
    'WPS428',  # Found statement that has no effect
)

DEFAULT_PYLINT_IGNORES = (
    'C0103',  # invalid-name
    'C0114',  # missing-module-docstring
    'C0115',  # missing-class-docstring
    'C0116',  # missing-function-docstring
    'E0602',  # undefined-variable
    'R0201',  # no-self-use
    'R0903',  # too-few-public-methods
    'W0104',  # pointless-statement
    'W0612',  # unused-variable
)


class LinterRunner:
    default_ignores: Iterable[str] = ()

    def get_error_pattern(self) -> Pattern[str]:
        raise NotImplementedError()

    def run(self, path: pathlib.Path, ignores: ErrorCodes = None) -> List[str]:
        if ignores is None:
            ignores = self.default_ignores
        ignores_str = ','.join(ignores)

        try:
            subprocess.check_output(self._get_command(str(path), ignores_str))
        except subprocess.CalledProcessError as exception:
            return self._parse_error_codes(exception.output.decode('utf-8'))
        else:
            return []

    def _get_command(self, path: str, ignores: str) -> List[str]:
        raise NotImplementedError()

    def _parse_error_codes(self, output: str) -> List[str]:
        errors = output.split('\n')
        error_codes = []
        for error in errors:
            match_result = self.get_error_pattern().match(error)
            if match_result:
                error_codes.append(match_result.group('code'))
        return error_codes


class Flake8Runner(LinterRunner):
    default_ignores: Iterable[str] = DEFAULT_FLAKE8_IGNORES

    def get_error_pattern(self) -> Pattern[str]:
        return FLAKE8_ERROR_PATTERN

    def _get_command(self, path: str, ignores: str) -> List[str]:
        return [
            'flake8',
            '--config={0}'.format(PROJECT_ROOT.joinpath('setup-test.cfg')),
            '--ignore={0}'.format(ignores),
            '--no-isort-config',
            path,
        ]


class PylintRunner(LinterRunner):
    default_ignores: Iterable[str] = DEFAULT_PYLINT_IGNORES

    def get_error_pattern(self) -> Pattern[str]:
        return PYLINT_ERROR_PATTERN

    def _get_command(self, path: str, ignores: str) -> List[str]:
        return [
            'pylint',
            '--rcfile={0}'.format(PROJECT_ROOT.joinpath('.pylintrc-test')),
            '--disable={0}'.format(ignores),
            path,
        ]


def run_flake8(path: pathlib.Path, ignores: ErrorCodes = None) -> List[str]:
    return Flake8Runner().run(path, ignores)


def run_pylint(path: pathlib.Path, ignores: ErrorCodes = None) -> List[str]:
    return PylintRunner().run(path, ignores)


def param_wrapper(
    content: Union[str, Sequence[str]],
    flake8_errors: Set[str],
    pylint_errors: Set[str],
    *, id: str,
) -> ParameterSet:
    if not isinstance(content, str):
        content = '\n'.join(content)
    content = '{0}\n'.format(content)
    return pytest.param(content, flake8_errors, pylint_errors, id=id)
