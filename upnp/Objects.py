# -*- coding: utf-8 -*-

class _BaseObj:
    """
    Base object with dict initialisation

    """
    def __init__(self, obj=None):
        if obj == None:
            return

        for atr in obj:
            if hasattr(self, atr):
                setattr(self, atr, obj[atr])

class Device(_BaseObj):
    """
    An UPnP device on the Network
    """
    def __init__(self, obj=None):
        """
        Device object initialisation
        :param obj: A dict with attributes
        """
        self.services = []
        self.devices = []
        self.icons = []
        self.uuid = ''
        self.st = ''
        self.deviceType = ''
        self.friendlyName = ''
        self.manufacturer = ''
        self.manufacturerURL = ''
        self.Description = ''
        self.modelName = ''
        self.modelNumber = ''
        self.upc = ''
        self.presentationURL = ''

        super(Device, self).__init__(obj)

    def addService(self, service):
        """
        Add a service on this device
        :param service: The service to add
        :type service: upnp.Service
        """
        self.services.append(service)

    def addDevice(self, device):
        """
        Add an embedded device
        :param device: The embedded device to add
        :type device: upnp.Device
        """
        self.devices.append(device)

class Icon(_BaseObj):
    """
    An device icon
    (don't work on Windows)
    """
    def __init__(self, obj=None):
        self.width = 32
        self.height = 32
        self.depth = 24
        self.mimetype = 'image/png'

        super(Icon, self).__init__(obj)

class Service(_BaseObj):
    """
    A service on a device
    """
    def __init__(self, obj=None):
        """
        Service object initialisation
        """
        self.serviceType = ''
        self.serviceId = ''
        self.SCPDURL = ''
        self.controlURL = ''
        self.eventSubURL = ''

        super(Service, self).__init__(obj)
