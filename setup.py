from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mskcc-csv-formatter',
    version='1.0.0',
    description='A Python script that takes a csv file as input and produces a required formatted file as output',
    url='https://github.com/moki298/mskcc-csv-formatter',
    author='Mohan Krishna Balli',
    author_email='moki298@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience:: Genomic Lab technologists at Memorial Sloan Kettering Cancer Center',
    ],
    keywords='utility tool',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
)
