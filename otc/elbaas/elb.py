from novaclient import base

class Elb(base.Resource):
    pass

class ElbManager(base.Manager):
    resource_class = Elb

    def list(self, vpcid=None, limit=1024):
        url = "/v1.0/{}/elbaas/loadbalancers?limit={}".format(
            self.api.projectid,
            limit,
        )
        if vpcid is not None:
            uri += "&vpc_id={}".format(vpcid)
        return self._list(url, 'loadbalancers')


class OtcElb(object):
    def __init__(self, otclient):
        self._otc = otcclient

    @property
    def otcclient(self):
        return self._otc

    def elbs(self, vpc=None, limit=1024):
        """Look up elbs"""
        requri = "{}/v1.0/{}/elbaas/loadbalancers?limit={}".format(
            self.elbaas_enpoint,
            self._projectid,
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
            self._projectid
        )
        if elb is not None:
            elbid = self.elb(elb)[0]['id']
            requri += "?loadbalancer_id={}".format(elbid)
    
        reqheaders = {
            "Content-Type":    "application/json",
            "Accept":           "application/json",
            "X-Language":       "en-us",
            "X-Auth-Token":     self._token,
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

