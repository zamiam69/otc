import otc.base

class Vpc(otc.base.Resource):
    pass

class VpcManager(otc.base.ResourceManager):
    resource_class = Vpc

    def list(self, limit=1024):
        url = """/v1/{}/vpcs?limit={}""".format(self.api.projectid, limit)
        return self._list(url, 'vpcs')

# vim: sw=4 sts=4 ts=4 et:
