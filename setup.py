                                                                                                                               
from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='pluggable-django-base',
      version=version,
      description="",
      long_description="""                                                                                                                                                     
""",
      classifiers=[],
      keywords='',
      author='Ethan Jucovy',
      author_email='ethan.jucovy@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
      "dj-database-url",
      
      ],
      entry_points="""  """,
      )
