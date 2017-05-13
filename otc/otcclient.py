import otc
import vpc.vpc as vpc
import elbaas.elb as elb

import re

re_UUID844412 = re.compile(r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$')
re_UUID = re.compile(r'^[0-9a-f]{32}$')

class OtcClient(object):
    def __init__(self, cloud_config=None, catalog=None, project_id=None,
        management_url=None,
        *args, **kwargs):
        self.projectid = project_id
        self.catalog = catalog
        self.cloud_config = cloud_config

        self.client = otc._construct_http_client(
            self.cloud_config.config['auth']['username'],
            self.cloud_config.config['auth']['password'],
            self.projectid,
            auth_token=kwargs['auth_token'],
            auth_url=self.cloud_config.config['auth']['auth_url'],
            service_type='network',
            service_catalog=catalog,
            service_url=self.service_url,
            )
        self.client.set_management_url(management_url)

    @property
    def service_url(self):
        endpoints = [ep for e in self.catalog 
                        for ep in e['endpoints'] 
                        if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")

        return endpoints[0]['url']


class VpcClient(OtcClient):
    def __init__(self, *args, **kwargs):
        super(VpcClient, self).__init__(*args, **kwargs)
        self.vpc = vpc.VpcManager(self)

class ElbClient(OtcClient):
    def __init__(self, *args, **kwargs):
        super(ElbClient, self).__init__(*args, **kwargs)
        self.elb = elb.ElbManager(self)

    @property
    def service_url(self):
        return super(ElbClient, self).service_url.replace('vpc', 'elb', 1)
 

# vim: sts=4 sw=4 ts=4 et:
