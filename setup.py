from setuptools import setup
from os import sep
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    version='1.1',
    description='Scraping images from the web.',
    author='Erich Garcia',
    author_email='erich.info.work@gmail.com',
    name='engineCrawler',
    packages=[
        'engineCrawler'
    ],
    install_requires=[
        'selenium',
        'requests',
        'imagehash',
        'PySocks!=1.5.7,>=1.5.6'
    ],
    scripts=['engineCrawler' + sep + 'imageCrawler.py'],
    keywords=[
        'crawler', 'scraping', 'search engines',
        'artificial intelligence',
        'databases', 'images'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Database",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)