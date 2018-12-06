#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='boisbot',
    version='0.1',
    packages=find_packages(exclude=['test', 'test*.py']),
    scripts=['scripts/scrape.py', 'scripts/fit.py', 'scripts/predict.py',
             'scripts/restservice.py'],

    author='Sam',
    author_email='levinsamuel000@gmail.com',
    url='https://github.com/levinsamuel/boisbot',
    install_requires=[
        'keras',
        'tensorflow',
        'selenium',
        'numpy',
        'beautifulsoup4',
        'Flask',
        'flask-jsonpify',
        'flask-sqlalchemy',
        'flask-restful'
    ]
)
