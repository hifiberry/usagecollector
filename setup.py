from setuptools import setup, find_packages

import usagecollector

setup(name='usagecollector',
      version=usagecollector.__version__,
      description='Usage data collector',
      long_description='A collection of tools to collect and read usage data', 
      url='http://github.com/hifiberry/usagecollector',
      author='Daniel Matuschek',
      author_email='daniel@hifiberry.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],
      packages=find_packages(),
      install_requires=['bottle'],
      scripts=[],
      keywords='statistics, database',
      zip_safe=False)
