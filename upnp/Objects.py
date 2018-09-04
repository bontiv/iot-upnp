# -*- coding: utf-8 -*-

class Device:
    def __init__(self, obj=None):
        """
        Device object
        """
        self.services = []
        self.devices = []
        self.uuid = obj['uuid']

    def addService(self, service):
        self.services.append(service)

class Service:
    def __init__(self, obj=None):
        """
        Service object
        """
        pass
