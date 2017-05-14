import shade
import otc

class TestBasics:
    """Basic tests"""

    def setUp(self):
        self.cloud = otc.OtcCloud(cloud='test')

    def tearDown(self):
        pass

    def test_construction(self):
        """Test it can be set up"""
        assert isinstance(self.cloud, shade.OpenStackCloud)

    def test_shade_works(self):
        """Ensure shade methods are available"""
        images = self.cloud.list_images()
        assert len(images) >= 0

    def test_list_vpcs(self):
        """List OTC VPCs"""
        res = self.cloud.list_vpcs()
        assert len(res) >= 0

    def test_search_vpcs(self):
        """Search OTC VPCs"""
        res = self.cloud.search_vpcs('foo')
        assert len(res) >= 0

    def test_list_elbs(self):
        """List OTC ELBs"""
        res = self.cloud.list_elbs()
        assert len(res) >= 0

    def test_search_elbs(self):
        """Search OTC ELBs"""
        res = self.cloud.search_elbs('foo')
        assert len(res) >= 0

    def test_list_listeners(self):
        """List OTC ELB listeners"""
        res = self.cloud.list_listeners()
        assert len(res) >= 0

    def test_search_listeners(self):
        """Search OTC VPCs"""
        res = self.cloud.search_listeners('foo')
        assert len(res) >= 0

# vim: sts=4 sw=4 ts=4 et:
