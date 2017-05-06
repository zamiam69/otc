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
        self._otc_project_id = None
        self._otc_token = None
        self._otc_catalog = None
        self.otcclient = otcclient.OtcClient(self.cloud_config)

# vim: sts=4 sw=4 ts=4 et:
