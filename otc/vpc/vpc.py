from novaclient import base

class Vpc(base.Resource):
    pass

class VpcManager(base.Manager):
    resource_class = Vpc

    def list(self, limit=1024):
        url = """/v1/{}/vpcs?limit={}""".format(self.api.projectid, limit)
        return self._list(url, 'vpcs')

# vim: sw=4 sts=4 ts=4 et:
