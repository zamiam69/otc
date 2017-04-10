# Quickstart

## Requirements

- python-shade
- Working otc Openstack shell environment (`.ostackrc`, `openrc`, ...)

## Python Shell

### Test shade compatibility

This creates a cloud instance analogous to the `shade.openstack_cloud()` method.
list\_servers() is a method provided by shade and 

	$ python
	Python 2.7.12 (default, Nov 19 2016, 06:48:10)
	[GCC 5.4.0 20160609] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import otc
	>>> cloud = otc.OTCCloud()
	>>> cloud.list_servers()[0]
	Munch({'OS-EXT-STS:task_state': None, 'addresses': {u'0ff6d449-ee81-48e4-97d6-17a6ded01b9e': [{u'OS-EXT-IPS-MAC:mac_addr': u'fa:16:3e:ee:06:02', u'version': 4, u'addr': u'10.11.64.30', u'OS-EXT-IPS:type': u'fixed'}]}, 'image': {u'id': u'6e6971f6-0e2b-461d-88d9-a6bd873c73dd'}, 'networks': {u'0ff6d449-ee81-48e4-97d6-17a6ded01b9e': [u'10.11.64.30']}, 'OS-EXT-STS:vm_state': u'active', 'OS-EXT-SRV-ATTR:instance_name': u'instance-00053e9d', 'OS-SRV-USG:launched_at': u'2017-04-06T12:19:36.360098', 'NAME_ATTR': 'name', 'flavor': {u'id': u'normal2'}, 'az': u'eu-de-02', 'id': u'9ff7c276-aa9b-459f-b168-ee5ab29dc513', 'security_groups': [{u'name': u'0ff6d449-ee81-48e4-97d6-17a6ded01b9e'}, {u'name': u'0ff6d449-ee81-48e4-97d6-17a6ded01b9e'}], 'user_id': u'b007aea1d4b34d4b9f17d3f1fbcce1f4', 'OS-DCF:diskConfig': u'MANUAL', 'HUMAN_ID': True, 'accessIPv4': u'', 'accessIPv6': u'', 'cloud': 'envvars', 'progress': 0, 'OS-EXT-STS:power_state': 1, 'OS-EXT-AZ:availability_zone': u'eu-de-02', 'config_drive': u'', 'status': u'ACTIVE', 'updated': u'2017-04-06T12:19:36Z', 'hostId': u'83cd392128f21ffcfec3f37ddd7f0a0a75a9df8006c8d052c9199da6', 'OS-EXT-SRV-ATTR:host': u'pod01.eu-de-02', 'OS-SRV-USG:terminated_at': None, 'key_name': u'work-default', 'request_ids': [], 'OS-EXT-SRV-ATTR:hypervisor_hostname': u'nova002@2', 'name': u'app00-bmp-ref', 'created': u'2017-04-06T12:19:08Z', 'tenant_id': u'4ac37b3b3fcc4585b045197fa31a15e7', 'region': 'eu-de', 'x_openstack_request_ids': [], 'os-extended-volumes:volumes_attached': [{u'id': u'56dfcd20-35fc-444e-b230-7951534c3136'}], 'volumes': [], 'metadata': {}, 'human_id': u'app00-bmp-ref'})

