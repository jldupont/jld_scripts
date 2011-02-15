#!/usr/bin/env python
"""
    Collection of python utility scripts

    @author: Jean-Lou Dupont
"""
__author__  ="Jean-Lou Dupont"
__version__ ="0.8.0"

from distutils.core import setup
from setuptools import find_packages

setup(name=         'jld_scripts',
      version=      __version__,
      description=  'Collection of python utility scripts',
      author=       __author__,
      author_email= 'jl@jldupont.com',
      url=          'http://www.systemical.com/doc/opensource/jld_scripts',
      package_dir=  {'': "src",},
      packages=     find_packages("src"),
      scripts=      ['src/scripts/m3u2symlinks', 'src/scripts/id3info', 'src/scripts/lastfm_gettracks'
                     ,'src/scripts/squeezecenter_utils'
                     ],
      package_data = {
                      '':[ "*.gif", "*.png", "*.jpg" ],
                      },
      include_package_data=True,                      
      zip_safe=False
      )
