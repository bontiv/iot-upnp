Quickstart
==========

.. toctree::
  :maxdepth: 2
  :hidden:

  dict
  attribute
  asyncio


IoT-UPnP require python 3.x. It use the following modules:
* asyncio: for the main event loop
* ssdp: base library for SSDP (a component of UPnP)
* netifaces: Network interfaces discovery (to retrieve IPs)

They are tree important objects:

.. autoclass:: upnp.Announcer

.. autoclass:: upnp.Device

.. autoclass:: upnp.Service

All objects can be set with theirs attributes or by passing a dict on the contructor.

Goal
----

UPnP device have services that need to be announced. Services can be controlled
and work as SOAP api. The class Announcer is used to anounce a device which have
one or many services.

On UPnP references, a device can also have many embedded devices.

To make a UPnP device, you need to make a service, add this service to a device
and them, announce this device as a root device.
