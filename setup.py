from setuptools import setup, find_packages

setup(name='dnurt_authors_integration',
      version='1.0.0',
      description='DNURT app for authors integration',
      long_description='',
      install_requires=['psycopg2', 'elsapy', 'wos', 'bs4'],
      url='https://github.com/ReturnedVoid/dnurt_authors_integration',
      author='Andrey Nechaev',
      author_email='andrewnech@gmail.com',
      license='DNURT',
      packages=find_packages(),
      keywords='DNURT author scopus web_of_science',

      entry_points={
          'console_scripts':
              ['authors_update = dnurt_integration.program:update']
      },
      package_data={
          '': ['*.json']
      }
      )
