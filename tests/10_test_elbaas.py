import otc

class TestElbClient:
    """ELB client tests"""

    def setUp(self):
        """Setup test cloud"""
        self.cloud = otc.OtcCloud(cloud='test')

    def tearDown(self):
        pass

    def test_elbclient_user_agent(self):
        assert self.cloud.elbclient.client.USER_AGENT == 'python-otcclient'

    def test_elbclient_elb(self):
        """List elbs"""
        elbs = self.cloud.elbclient.elb.list()
        assert len(elbs) >= 0

# vim: sts=4 sw=4 ts=4 et:
