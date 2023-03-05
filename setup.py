from setuptools import setup

setup(name='QRALib',
      version='0.3',
      description='Description ',
      url='https://github.com/samlothen/QRALib',
      author='Sam Löthén',
      author_email='sam@lothen.se',
      license='GNUv3',
      packages=['QRALib'],
      install_requires=[
          'numpy',
          'joblib',
          'torch',
          'typing',
          'plotly',
          'SALib',
          'pandas',
          'openpyxl'
      ],
      zip_safe=False)