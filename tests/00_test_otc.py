import otc

def test_shade_works():
    """Test shade works"""
    cloud = otc.OTCCloud()

def test_otc():
    """Basic Test"""
    cloud = otc.OTCCloud()
    images = cloud.list_images()
    assert len(images) >= 0

# vim: sts=4 sw=4 ts=4 et:
