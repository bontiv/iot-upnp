# -*- coding: utf-8 -*-

class Device:
    def __init__(self, obj=None):
        """
        Device object
        """
        self.services = []
        self.devices = []
        self.uuid = obj['uuid']
        self.st = 'upnp:rootdevice'
        self.deviceType = 'urn:sadmin-fr:device:demo:1'
        self.friendlyName = 'Demo UPnP Device'
        self.manufacturer = 'SADMIN'
        self.manufacturerURL = 'http://sadmin.fr'
        self.Description = 'Test for UPnP Device'
        self.modelName = 'UPnP-Demo'
        self.modelNumber = 'UPnP-1.0'
        self.upc = ''
        self.presentationURL = 'http://google.fr/'

    def addService(self, service):
        self.services.append(service)

    def addDevice(self, device):
        self.devices.append(device)

class Service:
    def __init__(self, obj=None):
        """
        Service object
        """
        pass
