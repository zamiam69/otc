import json
import requests

class OtcClient(object):
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
        self._cloud_config = cloud_config
        self._get_token()

    @property
    def cloud_config(self):
        return self._cloud_config

    @property
    def token(self):
        return self._token

    @property
    def catalog(self):
        return self._catalog

    @property
    def projectid(self):
        return self._projectid

    def vpcs(self, limit=1024):
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
