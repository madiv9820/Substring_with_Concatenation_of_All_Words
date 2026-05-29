"""🧭 This test file turns each JSON case into its own unittest so every
scenario gets clear pass/fail reporting, plus a small timeout guard.

Instead of putting all cases inside one big `test()` loop, we generate
one real test method per case. That way, `unittest` can show exactly
which scenario passed or failed in verbose mode. """

import json
import os
import sys
import time
import unittest
import unicodedata
from typing import List
from prettytable import PrettyTable
from timeout_decorator import TimeoutError, timeout
from source.solution import Solution


def _to_test_name(title: str) -> str:
    # 🏷️ Convert each friendly title into a safe unittest method name.
    # `unittest` expects names like `test_something`, so we clean the title
    # and turn spaces / emojis / punctuation into underscores.
    sanitized = ''.join(char.lower() if char.isalnum() else '_' for char in title)
    compact = '_'.join(part for part in sanitized.split('_') if part)
    return f'test_{compact}'


def _make_testcase(testcase):
    # 🧱 Build one real unittest method per JSON case for better test output.
    # This function returns another function, which becomes an actual test
    # method on `TestSolution`.
    def test_method(self):
        title: str = testcase['title']
        s: str = testcase['input']['s']
        words: List[str] = testcase['input']['words']
        expected_output: List[int] = testcase['output']
        description: str = testcase.get('description', 'No description provided.')

        # 🎬 Print a small intro card before each testcase begins.
        print('\n' + '=' * 60)
        print(f'🧪 Test Case : {title}')
        print(f'📝 Scenario  : {description}')
        print(f'🔤 String   : {s}')
        print(f'🧩 Words    : {words}')
        print('⏳ Starting soon...')
        time.sleep(self.DISPLAY_DELAY_SECONDS)

        try:
            # ▶️ Run the solution for this specific case under the timeout guard.
            actual_output: List[int] = self._run_case(s=s, words=words)
        except TimeoutError:
            # ⏱️ Turn timeout exceptions into normal unittest failures.
            print(f'⏱️ Result    : Time Limit Exceeded in {title}')
            print('=' * 60)
            self.fail(f'⏱️ Time Limit Exceeded: {title}')

        # ✅ A passing case shows up naturally in verbose unittest output.
        # If values differ, unittest prints the custom message below.
        if sorted(actual_output) == sorted(expected_output):
            print(f'✅ Result    : Passed with answer {actual_output}')
        else:
            print(f'❌ Result    : Expected {expected_output}, got {actual_output}')

        self._last_expected = expected_output
        self._last_actual = actual_output

        print('=' * 60)
        # 💤 Pause between tests so the output feels paced and readable.
        time.sleep(self.DISPLAY_DELAY_SECONDS)

        self.assertEqual(
            sorted(actual_output),
            sorted(expected_output),
            f'❌ Value Mismatch in {title}\n'
            f'Expected = {expected_output}\n'
            f'Actual   = {actual_output}'
        )

    test_method._title = testcase['title']
    return test_method


def _plain_table_text(value) -> str:
    text = str(value)
    normalized = unicodedata.normalize('NFKD', text)
    ascii_only = normalized.encode('ascii', 'ignore').decode('ascii')
    return ' '.join(ascii_only.split()) or '-'


def _fit_table_text(value, width: int) -> str:
    text = _plain_table_text(value)
    if len(text) <= width:
        return text
    if width <= 3:
        return text[:width]
    return text[: width - 3] + '...'


class SummaryTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.summary = []

    def _get_title(self, test):
        method = getattr(test, test._testMethodName)
        func = getattr(method, '__func__', method)
        return getattr(func, '_title', test._testMethodName)

    def addSuccess(self, test):
        expected = getattr(test, '_last_expected', [])
        actual = getattr(test, '_last_actual', [])
        self.summary.append((self._get_title(test), 'PASS', expected, actual, '-'))
        super().addSuccess(test)

    def addFailure(self, test, err):
        expected = getattr(test, '_last_expected', [])
        actual = getattr(test, '_last_actual', [])
        message = 'Value Mismatch'
        self.summary.append((self._get_title(test), 'FAIL', expected, actual, message))
        super().addFailure(test, err)

    def addError(self, test, err):
        expected = getattr(test, '_last_expected', [])
        actual = getattr(test, '_last_actual', [])
        message = 'Runtime Error'
        self.summary.append((self._get_title(test), 'ERROR', expected, actual, message))
        super().addError(test, err)


class TestSolution(unittest.TestCase):
    # 🎛️ Tweak this to make the test run faster or more cinematic.
    DISPLAY_DELAY_SECONDS = 1

    def setUp(self):
        # 🛠️ Each test gets a fresh solution instance to keep runs predictable.
        self.__solution = Solution()
        return super().setUp()

    @timeout(2)
    def _run_case(self, s: str, words: List[str]) -> List[int]:
        # ⚡ Give every testcase its own timeout instead of timing the whole file.
        # If one case is too slow, only that case fails.
        return self.__solution.findSubstring(s=s, words=words)


_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
_FILE_PATH = os.path.join(_CURRENT_DIRECTORY, 'cases.json')


with open(_FILE_PATH, mode='r', encoding='utf-8') as read_file:
    # 🧪 Register every case as a standalone test so verbose mode is meaningful.
    # `setattr(...)` adds methods like `test_classic_sliding_window_win`
    # directly onto the `TestSolution` class before the test runner starts.
    for testcase in json.load(read_file):
        setattr(TestSolution, _to_test_name(testcase['title']), _make_testcase(testcase))


def _print_summary(summary):
    print('\n' + '=' * 130)
    print('📊 Test Summary')
    print('=' * 130)

    table = PrettyTable()
    table.field_names = ['Test Case', 'Status', 'Expected', 'Actual', 'Note']
    table.align['Test Case'] = 'l'
    table.align['Status'] = 'c'
    table.align['Expected'] = 'l'
    table.align['Actual'] = 'l'
    table.align['Note'] = 'l'
    widths = {
        'Test Case': 34,
        'Status': 7,
        'Expected': 18,
        'Actual': 18,
        'Note': 18,
    }
    for column, width in widths.items():
        table.max_width[column] = width

    for title, status, expected, actual, message in summary:
        table.add_row([
            _fit_table_text(title, widths['Test Case']),
            _fit_table_text(status, widths['Status']),
            _fit_table_text(expected, widths['Expected']),
            _fit_table_text(actual, widths['Actual']),
            _fit_table_text(message, widths['Note']),
        ])

    print(table)

    passed = sum(1 for _, status, _, _, _ in summary if status == 'PASS')
    failed = len(summary) - passed
    print(f'✅ Passed: {passed}   ❌ Failed: {failed}')
    print('=' * 130)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSolution)
    runner = unittest.TextTestRunner(verbosity=2, resultclass=SummaryTestResult)
    result = runner.run(suite)
    _print_summary(result.summary)
    sys.exit(not result.wasSuccessful())
    