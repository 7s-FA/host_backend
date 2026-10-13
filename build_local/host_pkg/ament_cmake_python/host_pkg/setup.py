from setuptools import find_packages
from setuptools import setup

setup(
    name='host_pkg',
    version='0.0.0',
    packages=find_packages(
        include=('host_pkg', 'host_pkg.*')),
)
