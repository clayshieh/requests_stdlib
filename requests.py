import urllib
import urllib2
import json


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

    # process headers
    if not headers:
        headers = {}

    # process data
    if not data:
        data = {}

    request_obj = None

    # get request obj
    if data:
        request_obj = urllib2.Request(url, data=json.dumps(data), headers=headers)
    request_obj = urllib2.Request(url, headers=headers)

    # process method
    request_obj.get_method = lambda: method

    try:
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