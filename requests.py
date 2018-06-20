import urllib
import urllib2
import urlparse
import json
import httplib
import socket


# configurations
socket_scheme = "+unix"


# UNIX socket code
# referrenced from https://github.com/docker/docker-py/blob/master/docker/transport/unixconn.py
class UnixHTTPResponse(httplib.HTTPResponse, object):
    def __init__(self, sock, *args, **kwargs):
        disable_buffering = kwargs.pop('disable_buffering', False)
        kwargs['buffering'] = not disable_buffering
        super(UnixHTTPResponse, self).__init__(sock, *args, **kwargs)


class UnixHTTPConnection(httplib.HTTPConnection, object):

    def __init__(self, unix_socket, timeout=60):
        super(UnixHTTPConnection, self).__init__(
            'localhost', timeout=timeout
        )
        self.unix_socket = unix_socket
        self.timeout = timeout
        self.disable_buffering = False

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.unix_socket)
        self.sock = sock

    def putheader(self, header, *values):
        super(UnixHTTPConnection, self).putheader(header, *values)
        if header == 'Connection' and 'Upgrade' in values:
            self.disable_buffering = True

    def response_class(self, sock, *args, **kwargs):
        if self.disable_buffering:
            kwargs['disable_buffering'] = True

        return UnixHTTPResponse(sock, *args, **kwargs)


class CustomHTTPHandler(urllib2.HTTPHandler):
    """
    Custom HTTPHandler for urllib2 to communicate via unix sockets
    """

    def http_open(self, req):
        def genericHTTPConnection(host, port=None, strict=None, timeout=0):
            return UnixHTTPConnection(req._socket_path)
        return self.do_open(genericHTTPConnection, req)


# Requests code


class RequestResponse(object):
    def __init__(self, response):
        self.status_code = response.getcode()
        self.url = response.geturl()
        self.headers = response.headers.dict
        if isinstance(response, urllib2.HTTPError):
            self.text = response.reason
        else:
            self.text = response.read()
        response.close()

    def json(self):
        return json.loads(self.text)

def base_request(method, url, params=None, headers=None, data=None):
    # process url
    if params:
        query = urllib.urlencode(params)
        url += "?" + query

    # process if socket
    url_parts = urlparse.urlsplit(url)
    is_sock = socket_scheme in url_parts.scheme
    socket_path = None
    if is_sock:
        # get the socket path
        socket_path = urlparse.unquote(url_parts.netloc)
        # fix the scheme to play well with urllib2
        original_scheme = url_parts.scheme.replace(socket_scheme, "")
        url = url_parts._replace(scheme=original_scheme, netloc="localhost").geturl()

    # process headers
    if not headers:
        headers = {}

    # process data
    if not data:
        data = {}

    # get request obj
    request_obj = None
    if data:
        request_obj = urllib2.Request(url, data=json.dumps(data), headers=headers)
    request_obj = urllib2.Request(url, headers=headers)

    # process method
    request_obj.get_method = lambda: method

    # piggyback socket_path on request object
    if is_sock:
        request_obj._socket_path = socket_path

    # make http(s) connection
    try:
        if is_sock:
            response = urllib2.build_opener(CustomHTTPHandler).open(request_obj)
        else:
            response = urllib2.urlopen(request_obj)
    except urllib2.HTTPError as e:
        return RequestResponse(e)

    return RequestResponse(response)

def get(url, params=None, headers=None, data=None):
    return base_request("GET", url, params=params, headers=headers, data=data)


def post(url, params=None, headers=None, data=None):
    return base_request("POST", url, params=params, headers=headers, data=data)


def delete(url, params=None, headers=None, data=None):
    return base_request("DELETE", url, params=params, headers=headers, data=data)


def put(url, params=None, headers=None, data=None):
    return base_request("PUT", url, params=params, headers=headers, data=data)


