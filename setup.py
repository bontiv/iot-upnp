#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='iot-upnp',
    version='0.1',
    description='UPnP device annoncement library',
    author='Remi BONNET',
    author_email='bonnet@fanaticalhelp.com',
    url='https://sadmin.fr',
    packages=['upnp'],

    install_requires=[
        'ssdp',
        'netifaces',
    ]
)
