otc - python client library
===========================

OTC - the Open Telekom Cloud is an OpenStack fork by Huawei. For great parts
the API is shade compatible. Unfortunately some components are proprietary:

- Virtual Private Cloud VPC
- Elastic Load Balance ELB
- Elastic Cloud Service ECS

This library intends to make theses APIs accessible on top of shade.

----

Requirements
------------

- python-shade
- Working otc Openstack environment (.ostackrc, openrc, clouds.yaml, ...)

How to use it
-------------

Example::

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

Have a cloud 'test' in your *clouds.yaml*::

    ---
    clouds:
      test:
        auth:
          auth_url: https://iam.eu-de.otc.t-systems.com:443/v3
          user_name: USERNAME
          user_domain_name: USER_DOMAIN_NAME
          password: PASSWORD
          project_name: eu-de
        region_name: eu-de
        identity_api_version: 3
        volume_api_version: 2
        image_api_version: 2
        interface: publicURL

Replace USERNAME, USER_DOMAIN_NAME, PASSWORD accordingly. 

Then run::

    nosetest tests

