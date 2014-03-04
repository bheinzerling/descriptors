from setuptools import setup

name = 'descriptors'
version = '0.1.0'
author = 'Benjamin Heinzerling'
email = 'benjamin.heinzerling@openmailbox.org'
description = 'A collection of descriptors for validating input data.'
packages = ['descriptors']
scripts = []
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3"]

setup(
    name=name,
    version=version,
    author=author,
    author_email=email,
    packages=packages,
    scripts=scripts,
    url='https://github.com/noutenki/{}/'.format(name),
    license='LICENSE.txt',
    description=description,
    long_description=open('README.rst').read(),
    classifiers=classifiers
    )
