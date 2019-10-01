import pathlib
import re
import subprocess
from typing import Iterable, List, Optional

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.allof import AllOf
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]

FLAKE8_ERROR_PATTERN = re.compile(r'(?P<module>/tmp/.+\.py):(?P<line>\d+): \[(?P<code>[A-Z]+\d+)\] (?P<message>.+)')
PYLINT_ERROR_PATTERN = re.compile(r'(?P<module>/tmp/.+\.py):(?P<line>\d+):(?P<col>\d+): (?P<code>[A-Z]+\d+): (?P<message>.+) \((?P<verbose_code>[a-z\-]+)\)')  # noqa: E501 line too long


def run_flake8(path: pathlib.Path) -> List[str]:
    try:
        subprocess.check_output([  # noqa: S607 Tests will be executed in virtualenv with certain flake8 executable
            'flake8',
            '--config={0}'.format(PROJECT_ROOT.joinpath('setup-test.cfg')),
            str(path),
        ])
    except subprocess.CalledProcessError as exception:
        errors = exception.output.decode('utf-8').split('\n')
        error_codes = []
        for error in errors:
            match_result = FLAKE8_ERROR_PATTERN.match(error)
            if match_result:
                error_codes.append(match_result.group('code'))
        return error_codes
    else:
        return []


def run_pylint(path: pathlib.Path) -> List[str]:
    try:
        subprocess.check_output([  # noqa: S607 Tests will be executed in virtualenv with certain pylint executable
            'pylint',
            '--rcfile={0}'.format(PROJECT_ROOT.joinpath('.pylintrc-test')),
            str(path),
        ])
    except subprocess.CalledProcessError as exception:
        errors = exception.output.decode('utf-8').split('\n')
        error_codes = []
        for error in errors:
            match_result = PYLINT_ERROR_PATTERN.match(error)
            if match_result:
                error_codes.append(match_result.group('code'))
        return error_codes
    else:
        return []


ErrorCodes = Optional[Iterable[str]]


class CustomAllOf(AllOf):
    def matches(self, item, mismatch_description=None):
        for matcher in self.matchers:
            if not matcher.matches(item):
                if mismatch_description:
                    matcher.describe_mismatch(item, mismatch_description)
                return False
        return True


class BaseViolatesRules(BaseMatcher):
    has_error_msg = ''
    no_errors_msg = ''

    def __init__(self, errors: ErrorCodes = None):
        self.errors = set(errors) if errors is not None else set()
        # We need to keep produced codes to use them for mismatch message
        self.produced_codes: List[str] = []

    def describe_to(self, description):
        self._make_description(description, self.errors)

    def describe_mismatch(self, path: pathlib.Path, mismatch_description):
        mismatch_description.append_text('got ')
        self._make_description(mismatch_description, self.produced_codes)

    def _matches(self, path: pathlib.Path) -> bool:
        self.produced_codes = self._run_linter(path)
        return all(code in self.produced_codes for code in self.errors)

    def _make_description(self, description, errors: Iterable[str]):
        if errors:
            (
                description
                .append_text(self.has_error_msg)
                .append_text(' ')
                .append_text(', '.join(errors))
            )
        else:
            description.append_text(self.no_errors_msg)

    def _run_linter(self, path: pathlib.Path) -> List[str]:
        raise NotImplementedError


class ViolatesFlake8Rules(BaseViolatesRules):
    has_error_msg = 'Flake8 errors'
    no_errors_msg = 'no Flake8 errors'

    def _run_linter(self, path: pathlib.Path) -> List[str]:
        return run_flake8(path)


class ViolatesPylintRules(BaseViolatesRules):
    has_error_msg = 'Pylint errors'
    no_errors_msg = 'no Pylint errors'

    def _run_linter(self, path: pathlib.Path) -> List[str]:
        return run_pylint(path)


def violates_rules(*, flake8_errors: ErrorCodes = None, pylint_errors: ErrorCodes = None) -> BaseMatcher:
    return CustomAllOf(
        wrap_matcher(ViolatesFlake8Rules(flake8_errors)),
        wrap_matcher(ViolatesPylintRules(pylint_errors)),
    )
