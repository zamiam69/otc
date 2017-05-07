import json
import requests
import warnings

import re

re_UUID844412 = re.compile(r'^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$')
re_UUID = re.compile(r'^[0-9a-f]{32}$')

class OtcClient(object):
    """Client for the OTC API"""
    _token_req = {
        'auth': {
            'identity': {
                'methods': ['password'],
                'password': {
                    'user': {
                        'name': '',
                        'password': '',
                        'domain': {'name': ''},
                    },
                },
            },
            'scope': {
                'project': { 'name': '', },
            },
        }
    }

    def __init__(self, cloud_config, catalog=None, keystone_session=None):
        """Make os client config available and request an OTC API IAM Token"""
        self._cloud_config = cloud_config
        if catalog is None or keystone_session is None:
            self._get_token()
        else:
            self._catalog = catalog
            self._keystone_session = keystone_session

    @property
    def cloud_config(self):
        """OS client config"""
        return self._cloud_config

    @property
    def token(self):
        """OTC API Token, might be the same as the keystone token"""
        # return self._token
        return self._keystone_session.get_token()

    @property
    def catalog(self):
        """OTC catalog, apparently the same as keystone's"""
        return self._catalog

    @property
    def projectid(self):
        """OTC project id, required for OTC API requests. Also referred to as
           tenant_id in Huaweis documentation"""
        # return self._projectid
        return self._keystone_session.get_project_id()

    @property
    def elbaas_enpoint(self):
        endpoints = [ep for e in self.catalog 
                        for ep in e['endpoints'] 
                        if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")
        return endpoints[0]['url'].replace('vpc', 'elb', 1)

    def vpcs(self, limit=1024):
        """Look up all vpcs"""
        endpoints = [ep for e in self.catalog for ep in e['endpoints'] if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")

        requri = "{}/v1/{}/vpcs?limit={}".format(endpoints[0]['url'], self.projectid, limit)
        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self.token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            vpcs = resp.json()["vpcs"]
        except Exception, e:
			raise

        if resp.status_code == 200:
			return vpcs

        raise otc.OtcException(resp.headers)

    def vpc(self, vpc):
        """Get vpc by name or id"""
        lookup = 'id' if re_UUID844412.match(vpc) else 'name'

        vpcs = [v for v in self.vpcs() if v[lookup] == vpc]
        if len(vpcs) > 1:
            warnings.warn("vpc '{}' is not unique!".format(vpc))
        return vpcs


    def elbs(self, vpc=None, limit=1024):
        """Look up elbs"""
        requri = "{}/v1.0/{}/elbaas/loadbalancers?limit={}".format(
            self.elbaas_enpoint,
            self.projectid,
            limit)
        
        if vpc is not None:
            vpcs = self.vpc(vpc)
            if len(vpcs) == 0:
                vpcid = ""
            else:
                vpcid = vpcs[0]['id']
            requri += "&vpc_id={}".format(vpcid)

        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self.token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            elbs = resp.json()
        except Exception, e:
			raise

        if resp.status_code == 200:
			return elbs

        raise otc.OtcException(resp.headers)

    def elb(self, elb):
        """Lookup an elb by id or name"""
        lookup = 'id' if re_UUID.match(elb) else 'name'

        elbs = [e for e in self.elbs()['loadbalancers'] if e[lookup] == elb]
        if len(elbs) > 1:
            warnings.warn("elb '{}' is not unique!".format(elb))
        return elbs

    def elb_listeners(self, listener=None, elb=None):
        """Look up listeners"""
        requri = "{}/v1.0/{}/elbaas/listeners".format(
            self.elbaas_enpoint, 
            self.projectid
        )
        if elb is not None:
            elbid = self.elb(elb)[0]['id']
            requri += "?loadbalancer_id={}".format(elbid)

        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self.token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            listeners = resp.json()
        except Exception, e:
			raise

        if resp.status_code == 200:
            if listener is None:
                return listeners
            lookup = 'id' if re_UUID.match(listener) else 'name'
            return [l for l in listeners if l[lookup] == listener]

        raise otc.OtcException(resp.headers)

    def _get_token(self):
        try:
            req = OtcClient._token_req.copy()
            aa = self.cloud_config.get_auth_args()
            scope = req['auth']['scope']
            scope['project']['name'] = aa['project_name']
            user = req['auth']['identity']['password']['user']
            user['name'] = aa['username']
            user['password'] = aa['password']
            user['domain']['name'] = aa['user_domain_name'] 
            uri = self.cloud_config.config['auth']['auth_url'] + "/auth/tokens"
            resp = requests.post(
                uri,
                json=req,
                headers={'content-type': 'application/json'}
            ) 
        except Exception, e:
            raise

        if resp.status_code != 201:
            raise OtcException(resp.headers)

        jresp = resp.json()
        self._catalog = jresp['token']['catalog']
        self._projectid = jresp['token']['project']['id']
        self._token = resp.headers['X-Subject-Token']
    
# vim: sts=4 sw=4 ts=4 et:
