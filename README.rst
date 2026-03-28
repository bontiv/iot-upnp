.. list-table::
  :header-rows: 0
  :stub-columns: 1
  :widths: 30 70

  * - Builds
    - .. image:: https://travis-ci.org/bontiv/iot-upnp.svg?branch=master
        :target: https://travis-ci.org/bontiv/iot-upnp
        :alt: CI Status

      .. image:: https://readthedocs.org/projects/iot-upnp/badge/?version=latest
        :target: https://iot-upnp.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

  * - Code Quality
    - .. image:: https://codecov.io/gh/bontiv/iot-upnp/branch/master/graph/badge.svg
          :target: https://codecov.io/gh/bontiv/iot-upnp
          :alt: Coverage Status

      .. image:: https://sonarcloud.io/api/project_badges/measure?project=bontiv_iot-upnp&metric=sqale_rating
          :target: https://sonarcloud.io/dashboard?id=bontiv_iot-upnp
          :alt: Code maintainability

      .. image:: https://sonarcloud.io/api/project_badges/measure?project=bontiv_iot-upnp&metric=alert_status
          :target: https://sonarcloud.io/dashboard?id=bontiv_iot-upnp
          :alt: Code quality

  * - Releases information
    - .. image:: https://img.shields.io/pypi/status/iot-upnp.svg
          :alt: PyPI - Status
          :target: https://pypi.org/project/iot-upnp/

      .. image:: https://img.shields.io/pypi/format/iot-upnp.svg
          :alt: PyPI - Format
          :target: https://pypi.org/project/iot-upnp/#files

      .. image:: https://img.shields.io/pypi/v/iot-upnp.svg
          :alt: PyPI - Available version
          :target: https://pypi.org/project/iot-upnp/

  * - Package information
    - .. image:: https://img.shields.io/pypi/pyversions/iot-upnp.svg
          :alt: PyPI - Python versions
          :target: https://pypi.org/project/iot-upnp/#history

      .. image:: https://img.shields.io/github/license/bontiv/iot-upnp.svg
         :alt: GitHub license
         :target: https://github.com/bontiv/iot-upnp/blob/master/LICENSE

IoT UPnP
========
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

You need Python 3.5 or greater to use this library.

Usage and documentation
=======================

Installation
------------

You can use pip to install iot-upnp.

.. code::

   pip install iot-upnp


Full documentation
------------------

The full documentation are build with sphinx. It can be found on ReadTheDocs.
page : https://iot-upnp.readthedocs.io/.
