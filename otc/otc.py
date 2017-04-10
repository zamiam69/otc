from shade import *
import request

class OTCCloud(OpenStackCloud):
    """Wraps shade. Where shade can do an OTC job shade will be used.
OTC proprietary stuff will be dealt with in this module."""

    def __init__(self, *args, **kwargs):
        super(OTCCloud, self).__init__(*args, **kwargs)
        self.get_iam_token()

    def get_iam_token(self, *args, **kwargs):
        pass

# vim: sts=4 sw=4 ts=4 et:
