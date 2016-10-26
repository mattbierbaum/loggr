#from setuptools import setup
from distutils.core import setup

setup(name='loggr',
      license='MIT License',
      author='Matt Bierbaum',
      version='0.0.4',

      packages=['loggr'],
      install_requires=["tornado>=4.3"],
      scripts=['bin/loggr']
)
