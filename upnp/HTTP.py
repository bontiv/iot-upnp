# -*- coding: utf-8 -*-
import asyncio
from socket import gethostname

class HttpRequest:
    """
    HTTP Request informations
    """
    def __init__(self, method, path, version, headers):
        """
        Initiate a request

        :param method: HTTP request method
        :type method: str
        :param path: The requested path
        :type path: str
        :param version: HTTP version
        :type version: str
        :param headers: Dictionary of request headers
        :type headers: {str:str}
        """
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers

    def pprint(self):
        """
        Print human readable request
        """
        print('{} {} {}'.format(self.method, self.path, self.version))
        for h in self.headers:
            print ('  {}: {}'.format(h, self.headers[h]))
        print()

class HttpAnswer:
    """
    Class to construct an HTTP response
    """
    def __init__(self, request):
        """
        Initiate a response

        :param request: Origin request
        :type request: upnp.HTTP.HttpRequest
        """
        self.request = request
        self.statusCode = 200
        self.statusText = 'OK'
        self.version = 'HTTP/1.1'
        self.headers = {
            'Content-Type' : 'text/html; charset=utf8',
            'Server' : 'Linux UPnP/1.0 DoorDev/1.3-50131 (ZPS3)'
        }
        self.data = None

    def write(self, writer):
        """
        Send the response

        :param writer: Writer to send pakcet
        :type writer: asyncio.StreamWriter
        """
        writer.write('{} {} {}\r\n'.format(self.version, self.statusCode, self.statusText).encode('latin1'))
        for h in self.headers:
            writer.write('{}: {}\r\n'.format(h, self.headers[h]).encode('latin1'))
        writer.write(b'\r\n')
        if self.data != None:
            writer.write(self.data.encode('utf-8'))
            writer.write(b'\r\n')

    def pprint(self):
        """
        Show the packet as human readable
        """
        print('{} {} {}'.format(self.version, self.statusCode, self.statusText))
        for h in self.headers:
            print('  {}: {}'.format(h, self.headers[h]))
        print()

    def execute(self):
        """
        Need to be overrided by subclass. It's the execute process.
        """
        pass

class ServerErrorAnswer(HttpAnswer):
    """
    HTTP error response
    """
    def execute(self):
        """
        Prepare the response
        """
        self.statusCode = 500
        self.statusText = 'Internal Server Error'
        self.data = '<html><body><h1>Internal Server Error</h1><p>An internal server error. See logs.</p></body></html>'

class DescriptionAnswer(HttpAnswer):
    """
    HTTP success, describe a device (XML)
    """

    def __init__(self, request, upnp):
        """
        Initiate a device description

        :param request: Origin request
        :type request: upnp.HTTP.HttpRequest
        :param upnp: An UPnP configuration to describe
        :type upnp: upnp.UPnP.Announcer
        """
        super(DescriptionAnswer, self).__init__(request)
        self.upnp = upnp

    def describeDevice(self, device):
        """
        Add a device description to the answer

        :param device: Device to describe
        :type device: upnp.Objects.Device
        """

        self.data += """
        <device>
            <deviceType>{DEVICE.deviceType}</deviceType>
            <friendlyName>{DEVICE.friendlyName}</friendlyName>
            <manufacturer>{DEVICE.manufacturer}</manufacturer>
            <manufacturerURL>{DEVICE.manufacturerURL}</manufacturerURL>
            <modelDescription>{DEVICE.Description}</modelDescription>
            <modelName>{DEVICE.modelName}</modelName>
            <modelNumber>{DEVICE.modelNumber}</modelNumber>
            <UDN>uuid:{DEVICE.uuid}</UDN>
            <UPC>{DEVICE.upc}</UPC>
            <presentationURL>{DEVICE.presentationURL}</presentationURL>
            <iconList>
        """.format(DEVICE=device, CONFIGID=self.upnp.configId, URL=self.URL, HOST=self.HOST, HOSTNAME=self.HOSTNAME)
        for icon in device.icons:
            self.describeIcon(icon)

        self.data += """
        </iconList><serviceList>
        """
        for service in device.services:
            self.describeService(service)

        self.data += """
        </serviceList><deviceList>
        """
        for subdev in device.devices:
            self.describeDevice(subdev)
        self.data += """
        </deviceList></device>
        """


    def describeIcon(self, icon):
        """
        Add an icon description to the answer

        :param icon: Icon to describe
        :type icon: upnp.Objects.Icon
        """
        pass

    def describeService(self, service):
        """
        Add a service description to the answer

        :param service: Service to describe
        :type service: upnp.Objects.Service
        """

        self.data += """
        <service>
            <serviceType>{SERVICE.serviceType}</serviceType>
            <serviceId>{SERVICE.serviceId}</serviceId>
            <controlURL>{SERVICE.controlURL}</controlURL>
            <eventSubURL>{SERVICE.eventSubURL}</eventSubURL>
            <SCPDURL>{SERVICE.SCPDURL}</SCPDURL>
        </service>
        """.format(SERVICE=service)

    def execute(self):
        """
        Prepare the description answer
        """

        self.headers['Content-Type'] = 'application/xml; charset=utf-8'
        self.URL = 'http://{}'.format(self.request.headers['host'])
        self.HOST = self.request.headers['host'].split(':')[0]
        self.HOSTNAME = gethostname()

        self.data = """<?xml version="1.0"?>
        <root xmlns="urn:schemas-upnp-org:device-1-0" configId="{CONFIGID}">
            <specVersion>
                <major>1</major>
                <minor>0</minor>
            </specVersion>
        """.format(CONFIGID=self.upnp.configId)
        self.describeDevice(self.upnp.device)
        self.data += """
        </root>
        """

class ScpdAnswer(HttpAnswer):
    """
    HTTP success, Describe a service API

    """
    def __init__(self, request, upnp):
        """
        Initiate services to describe from the root device

        :param request: Origin request
        :type request: upnp.HTTP.HttpRequest
        :param upnp: An UPnP configuration to describe
        :type upnp: upnp.UPnP.Announcer
        """

        super(DescriptionAnswer, self).__init__(request)
        self.upnp = upnp

    def execute(self):
        """
        Prepare the answer
        """

        self.headers['Content-Type'] = 'application/xml; charset=utf-8'
        URL = 'http://{}'.format(self.request.headers['host'])

        self.data = """<?xml version="1.0"?>
        <scpd xmlns="urn:schemas-upnp-org:service-1-0" configId="CONFIGID">
            <specVersion>
                <major>1</major>
                <minor>0</minor>
            </specVersion>
            <actionList>
            </actionList>
        </scpd>
        """.format(UUID=UUID, URL=URL, CONFIGID=self.upnp.configId)

class HttpServer:
    """
    class to handle asyncio events on HTTP service
    """

    def __init__(self, config):
        """
        Initiate the HTTP server

        :param config: HTTP configuration
        :type config: upnp.HTTP.HTTP
        """
        self.config = config

    async def InConnection(self, reader, writer):
        """
        A new incomming connection

        :param reader: Request input
        :type reader: asyncio.StreamReader
        :param writer: Stream to answer
        :type writer: asyncio.StreamWriter
        """

        header = await reader.readline()
        cheaders = header.decode('latin1').strip()
        method, path, vers = cheaders.split(' ')
        headers = dict()

        while not reader.at_eof():
            rawheaders = await reader.readline()
            headline = rawheaders.decode('latin1').strip().lower()
            if headline == '':
                break
            head, value = headline.split(':', maxsplit=1)
            headers[head.strip()] = value.strip()

        request = HttpRequest(method, path, vers, headers)
        request.pprint()
        ans = self.HttpRouting(request)
        ans.execute()
        ans.pprint()
        ans.write(writer)
        writer.close()

    def HttpRouting(self, request):
        """
        A simple routing by path for incomming requests

        :param request: The incomming request
        :type request: upnp.HTTP.HttpRequest
        :return: The answer to execute
        :rtype: upnp.HTTP.HttpAnswer
        """

        if request.path == '/descr.xml':
            ans = DescriptionAnswer(request, self.config.annoncer)
        elif request.path == '/scpd.xml':
            ans = ScpdAnswer(request)
        else:
            ans = ServerErrorAnswer(request)
        return ans

class HTTP:
    """
    The main HTTP server class
    """

    def __init__(self, annoncer, port, netbind):
        """
        Initiate an HTTP Server

        :param annoncer: The UPnP configuration
        :type annoncer: upnp.UPnP.Announcer
        :param port: HTTP port
        :type port: int
        :param netbind: Interface address to bind
        :type netbind: str
        """

        self.port = port
        self.netbind = netbind
        self.server = None
        self.http_server = HttpServer(self)
        self.annoncer = annoncer

        if self.netbind == '0.0.0.0':
            self.netbind = None

    def initLoop(self, loop):
        """
        Add HTTP handlers on the asyncio loop

        :param loop: Loop to use
        :type loop: asyncio.AbstractEventLoop
        """

        self.server = asyncio.start_server(self.http_server.InConnection, port=self.port, host=self.netbind)
        self.httploop = loop.run_until_complete(self.server)

    def dispose(self):
        """
        Close HTTP handling
        """

        pass
