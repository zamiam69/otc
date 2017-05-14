import otc.base

class Elb(otc.base.Resource):
    pass

class ElbManager(otc.base.ResourceManager):
    resource_class = Elb

    def list(self, vpcid=None, limit=1024):
        url = "/v1.0/{}/elbaas/loadbalancers?limit={}".format(
            self.api.projectid,
            limit,
        )
        if vpcid is not None:
            url += "&vpc_id={}".format(vpcid)
        return self._list(url, 'loadbalancers')

# vim: sw=4 sts=4 ts=4 et:
