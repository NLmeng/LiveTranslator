#!/usr/bin/env python
import argparse
import os
import sys
import unittest
import shutil
import tempfile
import atexit

scripts_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(scripts_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

TMPDIR = tempfile.mkdtemp(prefix="tests_")

def cleanup_tmpdir():
    shutil.rmtree(TMPDIR, ignore_errors=True)

atexit.register(cleanup_tmpdir)

def run_tests(test_labels=None, verbosity=1, failfast=False, buffer=False):
    """Run unit tests with specified parameters."""
    loader = unittest.TestLoader()
    if test_labels:
        tests = loader.loadTestsFromNames(test_labels)
    else:
        tests = loader.discover('tests', pattern='tests_*.py')
    runner = unittest.TextTestRunner(verbosity=verbosity, failfast=failfast, buffer=buffer)
    return runner.run(tests)

def main():
    parser = argparse.ArgumentParser(description="Run all tests.")
    parser.add_argument('modules', nargs='*', metavar='module',
                        help='Optional path(s) to test modules; e.g. "preprocess.test_Preprocessor"')
    parser.add_argument('-v', '--verbosity', type=int, choices=[0, 1, 2, 3], default=1,
                        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_argument('--failfast', action='store_true', help='Stop on first failed test.')
    parser.add_argument('--buffer', action='store_true', help='Buffer stdout and stderr during test execution.')

    args = parser.parse_args()
    failures = run_tests(test_labels=args.modules, verbosity=args.verbosity, failfast=args.failfast, buffer=args.buffer)
    sys.exit(0 if failures.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
