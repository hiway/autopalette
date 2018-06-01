#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
)

import io
from glob import glob
from os.path import (
    basename,
    dirname,
    join,
    splitext,
)

from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
            join(dirname(__file__), *names),
            encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
        name='autopalette',
        version='0.1.0',
        license='BSD License',
        description='Terminal palettes and themes, without tears.',
        long_description=read('README.rst'),
        author='Harshad Sharma',
        author_email='harshad@sharma.io',
        url='https://github.com/hiway/autopalette',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data=True,
        zip_safe=False,
        classifiers=[
            # complete classifier list:
            # http://pypi.python.org/pypi?%3Aaction=list_classifiers
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: POSIX',
            'Operating System :: POSIX :: BSD',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Terminals',
            'Topic :: Software Development',
            'Topic :: Software Development :: User Interfaces',
            'Topic :: Utilities',
        ],
        keywords=[
            'terminal',
            'color',
            'theme',
            'palette',
        ],
        install_requires=[
            # MIT/ Felix Krull
            # https://pypi.org/project/colorhash/
            'colorhash>=1.0.2',

            # BSD License/ Valentin LAB
            # https://pypi.org/project/colour/
            'colour>=0.1.5',

            # ISCL/ Stefan Kögl
            # https://pypi.org/project/kdtree/
            'kdtree>=0.16',

            # Apache 2.0/ Felix Meyer-Wolters
            # https://pypi.org/project/sty/
            'sty>=1.0.0b6',

            # MIT/ Sam CB
            # https://pypi.org/project/emoji2text/
            'emoji2text',

            # MIT/ Rob Speer ( Luminoso )
            # https://pypi.org/project/ftfy/
            'ftfy',

            # WTFPL/ Micah Elliott
            # https://gist.github.com/MicahElliott/719710/
            # 'colortrans>=0.1',
            #  ^^ disabled since source is included with autopalette.
        ],
)
