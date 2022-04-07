from setuptools import setup, find_packages

setup(
    name='py_cc_ohlcv',
    version='0.0.4',
    license='MIT',
    author="Max Gao",
    author_email='gaamox@tutanota.com',
    packages=find_packages(exclude=["examples"]),
    url='https://github.com/gmax0/Cryptocurrency-OHLCV-Scraper',
    keywords='ohlcv, cryptocurrency, historical, market, data',
    install_requires=[
        'pandas',
        'requests'
      ],
)