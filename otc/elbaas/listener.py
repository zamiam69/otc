from novaclient import base

class Listener(base.Resource):
    pass

class ListenerManager(base.Manager):
    resource_class = Listener

    def list(self, elbid=None):
        url = "/v1.0/{}/elbaas/listeners".format(
            self.api.projectid,
        )
        if elbid is not None:
            url += "?loadbalancer_id={}".format(elbid)
        resp, data = self.api.client.get(url)
        items = [Listener(self, x, loaded=True) for x in data if x]
        return base.ListWithMeta(items, resp)

# vim: sts=4 sw=4 ts=4 et:
