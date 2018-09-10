# -*- coding: utf-8 -*-

import ssdp
import socket
import struct
import netifaces

class AnnouncerService(ssdp.SimpleServiceDiscoveryProtocol):
    """
    Endpoint for UDP packets (used by asyncio)
    """
    def __init__(self):
        """
        Initiate the UDP endpoint
        """
        self.annonces = None

    def connection_made(self, transport):
        """
        Called when the connection is made

        :param transport: The endpoint transport
        :type transport: asyncio.BaseTransport
        """
        self.transport = transport
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mreq = struct.pack("4sl", socket.inet_aton(self.MULTICAST_ADDRESS), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def response_received(self, response, addr):
        """
        Not used
        """
        # This will never been called (UDP)
        print("Response", addr)

    def request_received(self, request, addr):
        """
        Handle a new SSDP packet

        :param request: Request informations
        :param addr: Adress of the peer
        """
        if (request.method == 'M-SEARCH'):
            headers = dict()
            for (name, value) in request.headers:
                headers[name] = value

            if self.annonces.provides(headers['ST']):
                self.annonces.answer(headers['ST'], addr)

class Notify(ssdp.SSDPRequest):
    """
    SSDP Notify packet
    """

    def __init__(self, config, device):
        """
        Init a Notify packet

        :param config: An instance of SSDP service
        :type config: upnp.SSDP.SSDP
        :param device: A device to notify
        :type device: upnp.Device
        """
        self.transport = config.transport
        self.config = config
        self.nts = "ssdp:alive"
        self.nt = device.uuid
        self.uuid = device.uuid
        self.counter = 0
        self.location = 'http://ff:1900/description.xml'
        super(Notify, self).__init__('NOTIFY')

    def send(self, ip, usn = None, transport = None):
        """
        Build and send the packet

        :param ip: Destination IP
        :type ip: str
        :param usn: USN to notify
        :type usn: str
        :param transport: Transport to use
        :type transport: asyncio.BaseTransport
        """
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
        """
        Rewriting of raw sending method (error at the end of headers).

        :param transport: Transport to use
        :type transport: asyncio.BaseTransport
        :param addr: Destination address
        :type addr: str
        """
        msg = bytes(self) + b'\r\n\r\n'
        transport.sendto(msg, addr)
        self.config.srv.annonces.count = self.config.srv.annonces.count + 1

class Answer(ssdp.SSDPResponse):
    """
    Answer packet for M-SEARCH queries
    """

    def __init__(self, config, status_code, reason):
        """
        Initiate an SSDP answer

        :param config: SSDP configuration
        :type config: upnp.SSDP.SSDP
        :param status_code: Status code (like HTML)
        :type status_code: int
        :param reason: Text reason for status code
        :type reason: str
        """
        super(Answer, self).__init__(status_code, reason)
        self.config = config
        self.st = ''

    def send(self, device, ip, addr):
        """
        Send the UDP answer

        :param device: Device to announce
        :type device: upnp.Objects.Device
        :param ip: IP of device
        :type ip: str
        :param addr: Destination IP
        :type addr: str
        """
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
        """
        Rewriting of raw sending method (error at the end of headers).

        :param transport: Transport to use
        :type transport: asyncio.BaseTransport
        :param addr: Destination address
        :type addr: str
        """
        msg = bytes(self) + b'\r\n\r\n'
        transport.sendto(msg, addr)
        self.config.srv.annonces.count = self.config.srv.annonces.count + 1

class SSDP_Protocol:
    """
    Simple class to send packets
    """

    def __init__(self, config):
        """
        Create a new instance

        :param config: SSDP configuration
        :type config: upnp.SSDP.SSDP
        """
        self.config = config
        self.count = 1

    def notify(self, device, ip):
        """
        Send NOTIFY packets for a device (services and embedded devices)

        :param device: Device to announce
        :type device: upnp.Objects.Device
        :param ip: IP of the device
        :type ip: str
        """
        notify = Notify(self.config, device)
        notify.send(ip)

        for subdev in device.devices:
            notify.send(ip, subdev)

        for service in device.services:
            notify.send(ip, service)

    def answer(self, st, addr):
        """
        Answer to an M-SEARCH query

        :param st: Queried subject
        :type st: str
        :param addr: Destination address of answer
        :type addr: (str, int)
        """
        import locale, datetime

        message = Answer(self.config, 200, "OK")
        message.st = st
        #locale.setlocale(locale.LC_TIME, 'fr_FR')
        for device in self.getDevices(st):
            for ip in self.config.interfaces:
                message.send(device, ip, addr)

    def getDevices(self, st):
        """
        Get all devices which match ST

        :param st: Queried subject to match
        :type st: str
        :return: List of devices that match query
        :rtype: list(upnp.Objects.Device)
        """

        #root device
        if st == 'upnp:rootdevice':
            return [self.config.annoncer.device]

        devices = list()
        if self.config.annoncer.device.st == st:
            devices.append(self.config.annoncer.device)
        return devices

    def provides(self, usn):
        """
        Check if USN is provided by root device

        :param usn: USN to test
        :type usn: str
        :return: True if USN is provided
        :rtype: bool
        """
        if usn == 'upnp:rootdevice':
            return True

        if self.config.annoncer.device.st == usn:
            return True
        return False

class SSDP:
    """
    Public class to handle SSDP protocol
    """

    def __init__(self, annoncer, netBind='0.0.0.0'):
        """
        Initiate an SSDP endpoint

        :param annoncer: An announcer configuration
        :type annoncer: upnp.UPnP.Announcer
        :param netBind: Interface address to bind
        :type netBind: str
        """

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
        """
        Initiate an asyncio event loop

        :param loop: An asyncio event loop
        :type loop: asyncio.AbstractEventLoop
        """
        self.client = loop.create_datagram_endpoint(AnnouncerService, family=self.family, local_addr=(self.netbind, self.port))
        self.transport, self.srv = loop.run_until_complete(self.client)
        self.srv.annonces = SSDP_Protocol(self)

    def notify(self):
        """
        Send NOTIFY packets
        """
        for ip in self.interfaces:
            self.srv.annonces.notify(self.annoncer.device, ip)

    def dispose(self):
        """
        Close SSDP handling
        """
        self.transport.close()
