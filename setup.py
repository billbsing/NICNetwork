#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
from os.path import join

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

install_requirements = [
    'cairosvg',
    'networkx',
    'matplotlib',
    'pygal',
    'pygal_maps_world',
    'pycountry',
    'pypdf2',
    'scipy'
]

setup(
    author="billbsing",
    author_email='billbsing@gmail.com',
    classifiers=[
        'Development Status :: Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="NIC Network Charts",
    extras_require={
        'test': [],
        'docs': [],
        'dev': [],
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type='text/markdown',
    keywords='nic network',
    name='NICNetwork',
    packages=find_packages(),
    setup_requires=install_requirements,
    python_requires='>=3.6',
    url='https://github.com/billbsing/nic-charts',
    version='0.0.1',
    zip_safe=True,
)
