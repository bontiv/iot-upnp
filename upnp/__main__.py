#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import *

"""
This file is for test only.
"""

if __name__ == "__main__":
    import sys
    print('Starting test service UPnP')

    dev = Device({
        'deviceType': 'urn:sadmin-fr:device:demo:1',
        'friendlyName': 'UPnP Test',
        'uuid': '00a56575-78fa-40fe-b107-8f4b5043a2b0',
        'manufacturer': 'BONNET',
        'manufacturerURL': 'http://sadmin.fr'
    })

    dev.addService(Service({
        'serviceType': 'sadmin-fr:service:dummy',
        'serviceId': 'sadmin-fr:serviceId:1',
    }))

    upnpd = Annoncer(dev)
    upnpd.initLoop()
    upnpd.notify()
    upnpd.foreaver()
    upnpd.dispose()
