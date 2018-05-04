from setuptools import setup

setup(name='dnurt_authors_integration',
      version='1.0.0',
      description='DNURT app for authors integration',
      long_description='',
      install_requires=['psycopg2'],
      url='https://github.com/ReturnedVoid/dnurt_authors_integration',
      author='Andrey Nechaev',
      author_email='andrewnech@gmail.com',
      license='DNURT',
      packages=['dnurtdb', 'scopus', 'wos'],
      keywords='DNURT author scopus wos'
)