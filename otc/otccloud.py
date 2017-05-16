from shade import openstackcloud
from shade import _utils

import otcclient

class OtcCloud(openstackcloud.OpenStackCloud):

    """Wraps shade. Where shade can do an OTC job shade will be used.
    OTC proprietary stuff will be dealt with in this module."""

    def __init__(self, *args, **kwargs):
        super(OtcCloud, self).__init__(*args, **kwargs)
        # self._otc_client = None
        self._vpcclient = None
        self._elbclient = None
        self._ecsclient = None

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

    @property
    def ecsclient(self):
        if self._ecsclient is None:
            self._ecsclient = otcclient.EcsClient(
                cloud_config=self.cloud_config,
                catalog=self.service_catalog,
                project_id=self.project_id,
                auth_token=self.auth_token,
                management_url=self.management_url,
            )
        return self._ecsclient

    @staticmethod
    def by_name_or_id(resources, name_or_id):
        return [
            x for x in resources
            if x.id == name_or_id or x.name == name_or_id
        ]

    @_utils.cache_on_arguments()
    def list_ecs(self):
        return self.ecsclient.ecs.list()

    def search_ecs(self, name_or_id):
        return self.by_name_or_id(self.list_ecs(), name_or_id)

    @_utils.cache_on_arguments()
    def list_vpcs(self):
        return self.vpcclient.vpc.list()

    def search_vpcs(self, name_or_id):
        return self.by_name_or_id(self.list_vpcs(), name_or_id)

    @_utils.cache_on_arguments()
    def list_elbs(self):
        return self.elbclient.elb.list()

    def search_elbs(self, name_or_id):
        return self.by_name_or_id(self.list_elbs(), name_or_id)

    @_utils.cache_on_arguments()
    def list_listeners(self):
        return self.elbclient.listener.list()

    def search_listeners(self, name_or_id):
        return self.by_name_or_id(self.list_listeners(), name_or_id)

# vim: sts=4 sw=4 ts=4 et:
