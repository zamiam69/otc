from shade import *
import requests
import json
import otcclient

class OtcException(Exception):
    pass

class OtcCloud(OpenStackCloud):
    """Wraps shade. Where shade can do an OTC job shade will be used.
OTC proprietary stuff will be dealt with in this module."""

    def __init__(self, *args, **kwargs):
        super(OtcCloud, self).__init__(*args, **kwargs)
        self.otcclient = otcclient.OtcClient(
            self.cloud_config, 
            catalog=self.service_catalog,
            keystone_session=self.keystone_session)

# vim: sts=4 sw=4 ts=4 et:
