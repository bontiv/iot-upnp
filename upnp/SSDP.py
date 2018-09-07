# -*- coding: utf-8 -*-

import ssdp
import socket
import struct
import netifaces

class AnnouncerService(ssdp.SimpleServiceDiscoveryProtocol):

    def __init__(self):
        self.annonces = None

    def connection_made(self, transport):
        self.transport = transport
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mreq = struct.pack("4sl", socket.inet_aton(self.MULTICAST_ADDRESS), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def response_received(self, response, addr):
        # This will never been called (UDP)
        print("Response", addr)

    def request_received(self, request, addr):
        if (request.method == 'M-SEARCH'):
            headers = dict()
            for (name, value) in request.headers:
                headers[name] = value

            if self.annonces.provides(headers['ST']):
                self.annonces.answer(headers['ST'], addr)

class Notify(ssdp.SSDPRequest):
    def __init__(self, config, device):
        self.transport = config.transport
        self.config = config
        self.nts = "ssdp:alive"
        self.nt = device.uuid
        self.uuid = device.uuid
        self.counter = 0
        self.location = 'http://ff:1900/description.xml'
        super(Notify, self).__init__('NOTIFY')

    def send(self, ip, usn = None, transport = None):
        if (transport == None):
            transport = self.transport

        if usn == None:
            usn = 'uuid:' + self.uuid

        self.headers = [
            ('Host', '239.255.255.250'),
            ('LOCATION', 'http://' + ip + ':' + str(self.config.annoncer.http.port) + '/descr.xml'),
            ('NTS', self.nts),
            ('SERVER', ip),
            ('NT', self.nt),
            ('USN', usn),
            ('BOOTID.UPNP.ORG', self.config.srv.annonces.count),
            ('CONFIGID.UPNP.ORG', self.config.annoncer.configId),
        ]

        if self.counter > 0:
            self.headers.append(('BOOTID.UPNP.ORG', self.counter))

        if self.nts != 'ssdp:byebye':
            self.headers.append(('CACHE-CONTROL',  'max-age=' + str(self.config.maxage)))

        self.sendto(transport, (AnnouncerService.MULTICAST_ADDRESS, self.config.port))

    def sendto(self, transport, addr):
        msg = bytes(self) + b'\r\n\r\n'
        transport.sendto(msg, addr)
        self.config.srv.annonces.count = self.config.srv.annonces.count + 1

class Answer(ssdp.SSDPResponse):
    def __init__(self, config, status_code, reason):
        super(Answer, self).__init__(status_code, reason)
        self.config = config
        self.st = ''

    def send(self, device, ip, addr):
        import datetime

        self.headers = [
            ('CACHE-CONTROL',  'max-age=' + str(self.config.maxage)),
            ('DATE', datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')),
            ('ST', self.st),
            ('USN', device.uuid + '::' + device.st),
            ('EXT', ''),
            ('SERVER', self.config.signature),
            ('LOCATION', 'http://' + ip + ':' + str(self.config.annoncer.http.port) + '/descr.xml'),
            ('BOOTID.UPNP.ORG', self.config.srv.annonces.count),
            ('CONFIGID.UPNP.ORG', self.config.annoncer.configId),
        ]
        self.sendto(self.config.transport, addr)

    def sendto(self, transport, addr):
        msg = bytes(self) + b'\r\n\r\n'
        transport.sendto(msg, addr)
        self.config.srv.annonces.count = self.config.srv.annonces.count + 1

class SSDP_Protocol:
    def __init__(self, config):
        self.config = config
        self.count = 1

    def notify(self, device, ip):
        notify = Notify(self.config, device)
        notify.send(ip)

        for subdev in device.devices:
            notify.send(ip, subdev)

        for service in device.services:
            notify.send(ip, service)

    def answer(self, st, addr):
        import locale, datetime

        message = Answer(self.config, 200, "OK")
        message.st = st
        #locale.setlocale(locale.LC_TIME, 'fr_FR')
        for device in self.getDevices(st):
            for ip in self.config.interfaces:
                message.send(device, ip, addr)

    def getDevices(self, st):
        #root device
        if st == 'upnp:rootdevice':
            return [self.config.annoncer.device]

        devices = list()
        if self.config.annoncer.device.st == st:
            devices.append(self.config.annoncer.device)
        return devices

    def provides(self, usn):
        if usn == 'upnp:rootdevice':
            return True

        if self.config.annoncer.device.st == usn:
            return True
        return False

class SSDP:
    def __init__(self, annoncer, netBind='0.0.0.0'):
        self.annoncer = annoncer
        self.port = 1900
        self.family = socket.AF_INET
        self.netbind = netBind
        self.maxage = 3600
        self.signature = 'Linux UPnP/1.0 iot-UPnP/0.1'
        self.interfaces = []

        if netBind == '0.0.0.0':
            for iface in netifaces.interfaces():
                try:
                    if netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'] == '127.0.0.1':
                        continue
                    self.interfaces.append(netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr'])
                except KeyError:
                    pass
        else:
            self.interfaces = [netBind]

    def initLoop(self, loop):
        self.client = loop.create_datagram_endpoint(AnnouncerService, family=self.family, local_addr=(self.netbind, self.port))
        self.transport, self.srv = loop.run_until_complete(self.client)
        self.srv.annonces = SSDP_Protocol(self)

    def notify(self):
        for ip in self.interfaces:
            self.srv.annonces.notify(self.annoncer.device, ip)

    def dispose(self):
        self.transport.close()
