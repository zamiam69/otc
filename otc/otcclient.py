import json
import requests
import warnings

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

    def __init__(self, cloud_config):
        """Make os client config available and request an OTC API IAM Token"""
        self._cloud_config = cloud_config
        self._get_token()

    @property
    def cloud_config(self):
        """OS client config"""
        return self._cloud_config

    @property
    def token(self):
        """OTC API Token, might be the same as the keystone token"""
        return self._token

    @property
    def catalog(self):
        """OTC catalog, apparently the same as keystone's"""
        return self._catalog

    @property
    def projectid(self):
        """OTC project id, required for OTC API requests"""
        return self._projectid

    def vpcs(self, limit=1024):
        """Look up all vpcs"""
        endpoints = [ep for e in self._catalog for ep in e['endpoints'] if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")

        requri = "{}/v1/{}/vpcs?limit={}".format(endpoints[0]['url'], self._projectid, limit)
        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self._token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            vpcs = resp.json()["vpcs"]
        except Exception, e:
			raise

        if resp.status_code == 200:
			return vpcs

        raise otc.OtcException(resp.headers)

    def vpc_byname(self, vpc_name):
        """Look up a vpc by name."""
        vpcs = [v for v in self.vpcs() if v['name'] == vpc_name]
        if len(vpcs) > 1:
            warnings.warn("vpc name '{}' is not unique!".format(vpc_name))
        return vpcs

    def elb(self, vpc="", limit=1024):
        """Look up elbs for a given vpc name"""
        endpoints = [ep for e in self._catalog for ep in e['endpoints'] if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")
        ep_elb = endpoints[0]['url'].replace('vpc', 'elb', 1)

        vpcs = self.vpc_byname(vpc)
        if len(vpcs) == 0:
            vpcid = ""
        else:
            vpcid = vpcs[0]['id']

        requri = "{}/v1.0/{}/elbaas/loadbalancers?vpc_id={}&limit={}".format(ep_elb, self._projectid, vpcid, limit)

        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self._token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            elbs = resp.json()
        except Exception, e:
			raise

        if resp.status_code == 200:
			return elbs

        raise otc.OtcException(resp.headers)

    def elb_byname(self, vpcname, elbname):
        """Find elbs by name for a given vpc"""
        vpcs = self.vpc_byname(vpcname)
        elbs = [e for e in self.elb(vpcs[0]['name'])['loadbalancers'] if e['name'] == elbname]
        if len(elbs) > 1:
            warnings.warn("elb name '{}' is not unique!".format(elbname))
        return elbs

    def elb_listeners(self, elbid):
        """Look up listeners for a given elb id"""
        endpoints = [ep for e in self._catalog for ep in e['endpoints'] if e['type'] == "network"]
        if len(endpoints) == 0:
            raise otc.OtcException("No network endpoint in otc catalog.")
        ep_elb = endpoints[0]['url'].replace('vpc', 'elb', 1)

        requri = "{}/v1.0/{}/elbaas/listeners?loadbalancer_id={}".format(ep_elb, self._projectid, elbid)

        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self._token,
        }

        try:
            resp = requests.get(requri, headers=reqheaders)
            elbs = resp.json()
        except Exception, e:
			raise

        if resp.status_code == 200:
			return elbs

        raise otc.OtcException(resp.headers)

    def elb_listeners_byelbname(self, vpcname, elbname):
        """Look up listeners for a given vpc name and elb name"""
        elbs = self.elb_byname(vpcname, elbname)
        return self.elb_listeners(elbs[0]['id'])

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
