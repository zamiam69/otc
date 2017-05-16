import munch

from novaclient import base, client

class Resource(base.Resource):
    """Base for OTC Resources"""

class ResourceManager(base.Manager):
    """Base for OTC Resource Managers"""
    pass

class HTTPClient(client.HTTPClient):
    USER_AGENT = 'python-otcclient'

    def __init__(self, *args, **kwargs):
        service_catalog = kwargs.pop('service_catalog')
        service_url = kwargs.pop('service_url')

        super(HTTPClient, self).__init__(*args, **kwargs)
        self.service_catalog = service_catalog
        self.service_url = service_url

    def get_service_url(self, service_type):
        return self.service_url

    def _cs_request(self, url, method, **kwargs):
        return super(HTTPClient, self)._cs_request(url, method, **kwargs)

def _construct_http_client(*args, **kwargs):
    return HTTPClient(*args, **kwargs)

