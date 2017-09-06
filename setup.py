#!/usr/bin/env python3

from setuptools import setup, find_packages
from encodetools.version import __version__


setup(name='encodetools',
      version=__version__,
      description='Command line interface for fetching ENCODE data',
      author='Xiao-Ou Zhang',
      author_email='kepbod@gmail.com',
      url='https://github.com/kepbod/encodetools',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      keywords='encode',
      packages=find_packages(),
      install_requires=[
          'requests',
      ],
      )
