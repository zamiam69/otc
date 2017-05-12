from novaclient import base

class Vpc(base.Resource):
    pass

class VpcManager(base.Manager):
    resource_class = Vpc

    def list(self, limit=1024):
        url = """/v1/{}/vpcs?limit={}""".format(self.api.projectid, limit)
        return self._list(url, 'vpcs')

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

def vpc(self, vpc):
    """Get vpc by name or id"""
    lookup = 'id' if re_UUID844412.match(vpc) else 'name'

    vpcs = [v for v in self.vpcs() if v[lookup] == vpc]
    if len(vpcs) > 1:
        warnings.warn("vpc '{}' is not unique!".format(vpc))
    return vpcs

