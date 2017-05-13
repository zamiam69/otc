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

# vim: sts=4 sw=4 ts=4 et:
