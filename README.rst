otc - python client library
===========================

OTC - the Open Telekom Cloud is an OpenStack fork by Huawei. For great parts
the API is shade compatible. Unfortunately some components are proprietary:

- Virtual Private Cloud VPC
- Elastic Load Balance ELB
- Elastic Cloud Service ECS

This library intends to make theses APIs accessible on top of shade.

----

How to use it
-------------

    import otc

    cloud = otc.OtcCloud()

    # All shade methods should be available
    cloud.list_servers()
    ...

    # OTC APIs
    cloud.otcclient.vpcs()
    ...

Testing
-------

Have a cloud 'test' in your *clouds.yaml*. Then run

    nosetest tests

