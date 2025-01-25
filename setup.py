from setuptools import setup, find_packages, Command

import usagecollector

class NoTestCommand(Command):
    """A no-op test command."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Skipping tests.")

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
      test_suite=None,
      packages=find_packages(),
      install_requires=['bottle'],
      scripts=[],
      keywords='statistics, database',
      zip_safe=False,
      cmdclass={'test': NoTestCommand},
)
