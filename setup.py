#from setuptools import setup
import os
import re
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

try:
    readme = read('README.md')
except IOError as e:
    readme = ''

setup(name='loggr',
      license='MIT License',
      author='Matt Bierbaum',
      url='https://github.com/mattbierbaum/loggr',
      version='0.0.6',

      packages=['loggr'],
      install_requires=["tornado>=4.3"],
      scripts=['bin/loggr'],

      description='Remote log platform with easy integration into Python logging.',
      long_description=readme,
)
