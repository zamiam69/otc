from shade import *
import requests
import json
import otcclient

import novaclient.client

class HTTPClient(novaclient.client.HTTPClient):
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

class OtcException(Exception):
    pass

class OtcCloud(OpenStackCloud):
    """Wraps shade. Where shade can do an OTC job shade will be used.
    OTC proprietary stuff will be dealt with in this module."""

    def __init__(self, *args, **kwargs):
        super(OtcCloud, self).__init__(*args, **kwargs)
        # self._otc_client = None
        self._vpcclient = None
        self._elbclient = None

    @property
    def auth_token(self):
        """Aka OTC IAM token"""
        return self.keystone_session.get_token()

    @property
    def project_id(self):
        """OTC project id, required for OTC API requests. Also referred to as
        tenant_id in Huaweis documentation"""

        return self.keystone_session.get_project_id()

    @property
    def management_url(self):
        return self.cloud_config.config['auth']['auth_url'] + '/auth/tokens'

    @property
    def vpcclient(self):
        if self._vpcclient is None:
            self._vpcclient = otcclient.VpcClient(
                cloud_config=self.cloud_config,
                catalog=self.service_catalog,
                project_id=self.project_id,
                auth_token=self.auth_token,
                management_url=self.management_url,
            )
        return self._vpcclient

    @property
    def elbclient(self):
        if self._elbclient is None:
            self._elbclient = otcclient.ElbClient(
                cloud_config=self.cloud_config,
                catalog=self.service_catalog,
                project_id=self.project_id,
                auth_token=self.auth_token,
                management_url=self.management_url,
            )
        return self._elbclient

    # @property
    # def otc_client(self):
    #     if self._otc_client is None:
    #         self._otc_client = otcclient.OtcClient(
    #             cloud_config=self.cloud_config,
    #             catalog=self.service_catalog,
    #             project_id=self.project_id,
    #             auth_token=self.auth_token,
    #             management_url=self.management_url,
    #         )
    #     return self._otc_client

# vim: sts=4 sw=4 ts=4 et:
