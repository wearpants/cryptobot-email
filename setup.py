#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -s')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='cryptobot-email',
    version='0.1.0',
    description='CryptoBot Email is an email bot that helps people learn how to use OpenPGP.',
    long_description=readme,
    author='EFF Tech Team',
    author_email='tech@eff.org',
    url='https://github.com/EFForg/cryptobot-email',
    packages=[
        'cryptobot_email',
    ],
    package_data={'cryptobot_email': ['templates/*']},
    install_requires=[
        'Jinja2',
    ],
    license="AGPLv3+",
    zip_safe=False,
    keywords=['cryptobot-email', 'pgp', 'email'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Communications :: Email',
    ],
    test_suite='test',
    entry_points = {"console_scripts": ["cryptobot_email = cryptobot_email:main"]},
)