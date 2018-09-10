.. IoT-UPnP documentation master file, created by
   sphinx-quickstart on Thu Sep  6 13:51:40 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to IoT-UPnP's documentation!
====================================
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
-----------

You need Python 3.x to use this library.

documentation
-------------

.. toctree::
   :maxdepth: 2

   quickstart/index
   apidoc/modules
   links
