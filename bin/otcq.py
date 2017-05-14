#!/usr/bin/env python
# coding: utf8

import argparse
import otc

import json
import yaml
import pprint

DESCRIPTION="""OTC command line tool
"""

def cmdout(args, result):
    data = [x.to_dict() for x in result]
    if args.json:
        return json.dumps(data, indent=2)
    elif args.yaml:
        return yaml.safe_dump(data,
            encoding='utf-8',
            default_flow_style=False, 
            indent=2)
    else:
        pprint.pprint(result)

def elb_do(cloud, args):
    res = cloud.list_elbs()
    if args.OPERATION == 'list':
        print cmdout(args, res)
    else:
        print "Operation not implemented: {}".format(args.OPERATION)

def vpc_do(cloud, args):
    res = cloud.list_vpcs()
    if args.OPERATION == 'list':
        print cmdout(args, res)
    else:
        print "Operation not implemented: {}".format(args.OPERATION)

crud_operations = dict(
    choices=['list', 'create', 'delete', 'update'],
    help='operate on resource',
)

ap = argparse.ArgumentParser(description=DESCRIPTION, conflict_handler='resolve')
ap.add_argument('CLOUD', help="A cloud defined in clouds.yaml")
output = ap.add_mutually_exclusive_group()
output.add_argument('--json', action='store_true')
output.add_argument('--yaml', action='store_true')

sp = ap.add_subparsers(help="OTC APIs")

ap_vpc = sp.add_parser('vpc', help='Virtual Private Cloud')
ap_elb = sp.add_parser('elb', help="Elastic Load Balancer")

ap_vpc.add_argument('OPERATION', **crud_operations)
ap_elb.add_argument('OPERATION', **crud_operations)

ap_vpc.set_defaults(apicmd=vpc_do)
ap_elb.set_defaults(apicmd=elb_do)

if __name__ == '__main__':
    args = ap.parse_args()

    cloud = otc.OtcCloud(cloud=args.CLOUD)
    args.apicmd(cloud, args)

# vim: sts=4 ts=4 sw=4 et:
