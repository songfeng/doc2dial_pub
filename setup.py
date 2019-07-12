# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='doc2dial',
    version='0.0.1',
    description='crowd-based chat agent apps',
    long_description='long_description',
    packages=find_packages(exclude=(
        'data', 'docs', 'downloads', 'examples', 'logs', 'tests')),
    url='',
    license='Apache-2.0'
)
