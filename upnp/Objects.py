# -*- coding: utf-8 -*-

class BaseObj:
    def __init__(self, obj=None):
        if obj == None:
            return

        for atr in obj:
            if hasattr(self, atr):
                setattr(self, atr, obj[atr])

class Device(BaseObj):
    def __init__(self, obj=None):
        """
        Device object
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
        self.services.append(service)

    def addDevice(self, device):
        self.devices.append(device)

class Icon(BaseObj):
    def __init__(self, obj=None):
        self.width = 32
        self.height = 32
        self.depth = 24
        self.mimetype = 'image/png'

        super(Icon, self).__init__(obj)

class Service(BaseObj):
    def __init__(self, obj=None):
        """
        Service object
        """
        self.serviceType = ''
        self.serviceId = ''
        self.SCPDURL = ''
        self.controlURL = ''
        self.eventSubURL = ''

        super(Service, self).__init__(obj)
