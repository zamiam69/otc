import otc

class TestVpcClient:
    """VPC client tests"""

    def setUp(self):
        """Setup test cloud"""
        self.cloud = otc.OtcCloud(cloud='test')

    def tearDown(self):
        pass

    def test_vcp_user_agent(self):
        """Check user agent"""
        assert self.cloud.vpcclient.client.USER_AGENT == 'python-otcclient'

    def test_vpcclient_vpc(self):
        """List vpcs"""
        vpcs = self.cloud.vpcclient.vpc.list()
        assert len(vpcs) >= 0

# vim: sts=4 sw=4 ts=4 et:
