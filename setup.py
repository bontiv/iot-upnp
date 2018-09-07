#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path, getenv

version = '0.1'
release = getenv('TRAVIS_TAG', '0.1.dev10')
cmdclass = {}
cmdopts = {}

#Using Shinx documentation
try:
    from sphinx.setup_command import BuildDoc
    import os.path

    class GitlabDocs(BuildDoc):
        def finalize_options(self):
            super(GitlabDocs, self).finalize_options()
            self.builder_target_dirs = [(builder, self.build_dir if builder == 'html' else os.path.join(self.build_dir, builder)) for builder in self.builder]
            print(self.builder_target_dirs)


    cmdclass['build_docs'] = GitlabDocs
    cmdopts['build_docs'] = {
        'project': ('setup.py', 'IoT-UPnP'),
        'version': ('setup.py', version),
        'release': ('setup.py', release),
        'source_dir' : ('setup.py', 'docs.src'),
        'build_dir' : ('setup.py', 'docs')
    }
except ImportError:
    print("You must install Sphinx for documentation generation")

#README
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

#Main setup
setup(name='iot-upnp',
    version=release,
    description='UPnP device annoncement library',
    author='Remi BONNET',
    author_email='bonnet@fanaticalhelp.com',
    packages=['upnp'],
    license = 'GPLv3',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking'
    ],
    keywords='upnp ssdp network',
    python_requires='>3.0',
    url='https://github.com/bontiv/iot-upnp',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    project_urls={
        'Documentation': 'https://bontiv.github.io/iot-upnp/',
        'Tracker': 'https://github.com/bontiv/iot-upnp/issues'
    },
    install_requires=[
        'ssdp',
        'netifaces',
    ],

    extras_require={
        'docs': ['sphinx']
    },

    cmdclass=cmdclass,
    command_options=cmdopts
)
