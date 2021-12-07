#!/usr/bin/env python

from distutils.core import setup

setup(name='CS',
      version='1.0',
      description='Python utility to calculate and vizualize coverage and specificity',
      author='Yaroslav Plaksin',
      url='https://github.com/goxan/coverage-specificity',
      author_email='y.plaksin@innopolis.university',
      packages=['cov_spec'],
      install_requires=['validclust']
     )
