#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from setuptools import setup

try:
    # Python 3
    from os import dirname
except ImportError:
    # Python 2
    from os.path import dirname

here = os.path.abspath(dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

install_requires = []
tests_require = [
    'pytest>=3.0.6,<3.1.0',
]

setup(
    name='invisible-ink',
    version='0.1',
    description='Embedded messages in text for Python.',
    long_description=long_description,
    author='David Gouldin',
    author_email='david@gould.in',
    url='https://github.com/dgouldin/invisible-ink',
    py_modules=['invisible_ink'],
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
    },
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
