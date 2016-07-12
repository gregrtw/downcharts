from setuptools import setup
from setuptools.command.test import test as TestCommand

import sys
import os

import downcharts

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []

    for fn in filenames:
        with open(fn, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.md')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='downcharts',
    version=downcharts.__version__,
    url="https://github.com/gregrtw/downcharts",
    license="Restrictive License",
    author="Gregory Houle, Hans Daigle",
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    author_email='houle.greg@gmail.com, hansdaigle@me.com',
    description="Download Top Charting Music",
    long_description=long_description,
    packages=['downcharts'],
    include_package_data=True,
    platforms='any',
    test_suite='downcharts.test.test_downcharts',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'Operating System :: OS Independent'
    ],
    extras_require={
        'testing': ['pytest'],
    },
    scripts=[
        'downcharts/downcharts.py'
    ],
)
