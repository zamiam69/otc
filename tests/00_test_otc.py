import otc

def test_shade_works():
    """Test shade works"""
    cloud = otc.OtcCloud(cloud='test')

def test_otc():
    """Basic Test"""
    cloud = otc.OtcCloud(cloud='test')
    images = cloud.list_images()
    assert len(images) >= 0

def test_otcclient_client():
    cloud = otc.OtcCloud(cloud='test')
    assert cloud.otc_client.client.USER_AGENT == 'python-otcclient'
    
def test_otcclient_vpc_list():
    cloud = otc.OtcCloud(cloud='test')
    vpcs = cloud.otc_client.vpc.list()
    assert len(vpcs) >= 0

# vim: sts=4 sw=4 ts=4 et:
