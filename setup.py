from setuptools import setup, find_packages

setup(
    name="boisbot",
    version="0.1",
    packages=find_packages(exclude=['test*.py']),
    scripts=['scraper.py'],
    
    author="Sam",
    author_email="levinsamuel000@gmail.com",
    url="https://github.com/levinsamuel/boisbot",
    install_requires=[
        'keras',
        'tensorflow',
        'selenium',
        'beautifulsoup4'
    ]
)