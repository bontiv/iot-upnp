IoT UPnP
========

.. image:: https://travis-ci.org/bontiv/iot-upnp.svg?branch=master
    :target: https://travis-ci.org/bontiv/iot-upnp
.. image:: https://readthedocs.org/projects/iot-upnp/badge/?version=latest
    :target: https://iot-upnp.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://codecov.io/gh/bontiv/iot-upnp/branch/master/graph/badge.svg
      :target: https://codecov.io/gh/bontiv/iot-upnp
      
This project is a little pure Python library to annonce a device by
UPnP. It’s made for IoT developers to let them show their device on
network discovery in any OS.

With IoT-UPnP, you can show your device on all computers with Windows
Explorer (network discovery). Users can doucle-click on the device to
open the device configuration page. The device will be shown without any
software installation on user’s computers.

Developers can use UPnP to announce custom services and let others
applications use these services. For example, if cameras announce a
service “exemple-org:service:camera-image”, you can made a software
witch easy discover all cameras with this service.

Requirement
===========

You need Python 3.x to use this library.

Documentation
=============

Quick start
-----------

Installation
~~~~~~~~~~~~

You can use pip to install iot-upnp.

::

   pip install iot-upnp

Usage
~~~~~

The module is ``upnp``. You need to create a device with a service and
announce the device.

::

   import upnp

   device = upnp.Device()
   device.deviceType = 'run-sadmin-fr:device:demo:1'
   device.friendlyName = 'Demo UPnP Device'
   device.manufacturer = 'Bontiv'
   device.manufacturerURL = 'https://github.com/bontiv/'
   device.Description = 'A simple device witch open the project URL on double-click'
   device.modemName = 'DEMO-UPnP'
   device.modelNumber = 'DEMO-1.0'
   device.presentationURL = 'https://bontiv.github.io/iot-upnp/'

On the device we will make a new service.

::

   service = upnp.Service()
   device.addService(service)

Next we create the announcer. The announcer use the asyncio feature. You
can use the loop on your application or just use ``foreaver`` to run the
asyncio loop foreaver. It’s not mandatory but I advice you tou send a
NOTIFY event on the network to announce that your device is now
available.

::

    server = upnp.Annoncer(device)
    server.initLoop()
    server.notify()
    server.foreaver()
    server.dispose()

Full documentation
------------------

The full documentation are build with sphinx. It can be found on Github
page : https://bontiv.github.io/iot-upnp.
