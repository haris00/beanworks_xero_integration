#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='beanworks_xero_integration',
    version='1.0',
    author='',
    url='https://github.com/haris00/beanworks_xero_integration',
    description='',
    license='',
    packages=find_packages(),
    install_requires=['requests',
                      'Flask',
                      'oauthlib',
                      'Flask-Login',
                      'pyopenssl'],
    entry_points={}
)