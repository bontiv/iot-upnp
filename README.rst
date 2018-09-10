IoT UPnP
========

.. image:: https://travis-ci.org/bontiv/iot-upnp.svg?branch=master
    :target: https://travis-ci.org/bontiv/iot-upnp
.. image:: https://readthedocs.org/projects/iot-upnp/badge/?version=latest
    :target: https://iot-upnp.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://codecov.io/gh/bontiv/iot-upnp/branch/master/graph/badge.svg
      :target: https://codecov.io/gh/bontiv/iot-upnp
.. image:: https://sonarcloud.io/api/project_badges/measure?project=bontiv_iot-upnp&metric=sqale_rating
      :target: https://sonarcloud.io/dashboard?id=bontiv_iot-upnp
.. image:: https://sonarcloud.io/api/project_badges/measure?project=bontiv_iot-upnp&metric=alert_status
      :target: https://sonarcloud.io/dashboard?id=bontiv_iot-upnp

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

Installation
------------

You can use pip to install iot-upnp.

::

   pip install iot-upnp

::

Full documentation
------------------

The full documentation are build with sphinx. It can be found on ReadTheDocs.
page : https://iot-upnp.readthedocs.io/.
