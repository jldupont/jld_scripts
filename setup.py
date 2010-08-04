#!/usr/bin/env python
"""
    Collection of python utility scripts

    @author: Jean-Lou Dupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.1"

from distutils.core import setup
from setuptools import find_packages

setup(name=         'jld_scripts',
      version=      __version__,
      description=  'Collection of python utility scripts',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://www.systemical.com/',
      package_dir=  {'': "src",},
      packages=     find_packages(),
      scripts=      ['src/', 
                     ],
      )
