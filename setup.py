from setuptools import setup, find_packages
from pyexifwrangle import __version__

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
]

extra_dev = [
    *extra_test,
]

setup(
    name='pyexifwrangle',
    version=__version__,

    url='https://github.com/stephaniereinders/pyexifwrangle',
    author='Stephanie Reinders',
    author_email='reinders.stephanie@gmail.com',

    packages=find_packages(exclude=['tests', 'tests.*']),

    install_requires=[
        'pandas',
    ],

    extras_require={
        'dev': extra_dev,
    },
)
