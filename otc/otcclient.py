import otc
import vpc.vpc as vpc

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

        self.vpc = vpc.VpcManager(self)

        self.client = otc._construct_http_client(
            self.cloud_config.config['auth']['username'],
            self.cloud_config.config['auth']['password'],
            self.projectid,
            auth_token=kwargs['auth_token'],
            auth_url=self.cloud_config.config['auth']['auth_url'],
            service_type='network',
            service_catalog=catalog,
            )
        self.client.set_management_url(management_url)

#     @property
#     def elbaas_endpoint(self):
#         endpoints = [ep for e in self.catalog 
#                         for ep in e['endpoints'] 
#                         if e['type'] == "network"]
#         if len(endpoints) == 0:
#             raise otc.OtcException("No network endpoint in otc catalog.")
#         return endpoints[0]['url'].replace('vpc', 'elb', 1)
   
# vim: sts=4 sw=4 ts=4 et:
