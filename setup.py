from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class ToxTest(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments to pass down to Tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        import shlex

        args = []

        if self.tox_args:
            args = shlex.split(self.tox_args)

        sys.exit(tox.cmdline(args=args))


if __name__ == '__main__':
    setup(
        author='Alec Nikolas Reiter',
        name='twiki',
        author_email='alecreiter@gmail.com',
        license='MIT',
        packages=['twiki'],
        classifiers=['NOPE'],
        test_suite='tests',
        tests_require=['tox'],
        cmdclass={'test': ToxTest}
    )
