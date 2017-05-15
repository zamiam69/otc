import otc.base

class Ecs(otc.base.Resource):
    pass

class EcsManager(otc.base.ResourceManager):
    resource_class = Ecs

    def list(self, limit=1024):
        url = """/v2/{}/servers/detail?limit={}""".format(self.api.projectid, limit)
        return self._list(url, 'servers')

# vim: sw=4 sts=4 ts=4 et:
