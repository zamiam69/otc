import otc

def test_shade_works():
    """Test shade works"""
    cloud = otc.OtcCloud(cloud='test')

def test_otc():
    """Basic Test"""
    cloud = otc.OtcCloud(cloud='test')
    images = cloud.list_images()
    assert len(images) >= 0

def test_otcclient():
    """Test otcclient"""
    cloud = otc.OtcCloud(cloud='test')
    vpcs = cloud.otcclient.vpcs()
    assert len(vpcs) >= 0

def test_elb():
    """Test elbs"""
    cloud = otc.OtcCloud(cloud='test')
    elbs = cloud.otcclient.elbs()
    assert len(elbs) >= 0

def test_listeners():
    """Test listeners"""
    cloud = otc.OtcCloud(cloud='test')
    listeners = cloud.otcclient.elb_listeners()
    assert len(listeners) >= 0

# vim: sts=4 sw=4 ts=4 et:
