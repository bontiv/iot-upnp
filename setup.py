#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path, getenv

version = '1.0.4'
release = getenv('TRAVIS_TAG', '0.1.dev10')
cmdclass = {}
cmdopts = {}

#Using Shinx documentation
try:
    from sphinx.setup_command import BuildDoc

    cmdclass['build_docs'] = BuildDoc
    cmdopts['build_docs'] = {
        'project': ('setup.py', 'IoT-UPnP'),
        'version': ('setup.py', version),
        'release': ('setup.py', release),
        'source_dir' : ('setup.py', 'docs'),
        'build_dir' : ('setup.py', 'build')
    }
except ImportError:
    print("You must install Sphinx for documentation generation")

#README
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'docs', 'requirements.txt')) as f:
    docs_required = f.read().splitlines()

#Main setup
setup(
    version=release,
    cmdclass=cmdclass,
    command_options=cmdopts,
    extras_require={
        'docs' : docs_required
    }
)
