from distutils.core import setup

with open('README.rst') as f:
    ld = f.read()

setup(
    name='metallum_scraper',
    version='0.1',
    packages=['metallum_scraper', ],
    long_description=ld
)

