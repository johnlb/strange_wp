# coding: utf-8
"""
    strange
    ==========

    That's odd... why are you reading this?

"""

import re
import sys
import codecs
from os import path
from setuptools import setup, find_packages

VERSION = re.search("VERSION = '([^']+)'", codecs.open(
    path.join(path.dirname(__file__), 'strange', '__init__.py'),
    encoding="utf-8",
).read().strip()).group(1)

LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.rst')).read()


REQUIREMENTS = [
    # XXX: Keep this in sync with docs/install.rst
    'lxml>=3.0',
    'html5lib>=0.999999999',
    'tinycss==0.3',
    'cssselect>=0.6',
    'cffi>=0.6',
    'cairocffi>=0.5',
    'Pyphen>=0.8',
    'gdspy'
    # C dependencies: Gdk-Pixbuf (optional), Pango, cairo.
]

if sys.version_info < (3,):
    REQUIREMENTS.append('CairoSVG >= 1.0.20, < 2')
else:
    REQUIREMENTS.append('CairoSVG >= 1.0.20')

setup(
    name='strange',
    version=VERSION,
    # url='http://weasyprint.org/',
    license='GPL',
    description='Working towards a modernized analog circuit design toolchain.',
    long_description=LONG_DESCRIPTION,
    author='John Bell',
    author_email='john.l.bell@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Chip Designers',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    packages=find_packages(),
    package_data={
        'strange.hyphenation': ['*.dic'],
        'strange.tests': ['resources/*.*', 'resources/*/*'],
        'strange.css': ['*.css']},
    zip_safe=False,
    install_requires=REQUIREMENTS,
    test_suite='strange.tests',
    entry_points={
        'console_scripts': [
            'strange = strange.__main__:main',
        ],
    },
)
