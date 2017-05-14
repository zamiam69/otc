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
    if args.OPERATION == 'list':
        if args.ELB:
            res = cloud.search_elbs(args.ELB)
        else:
            res = cloud.list_elbs()
        print cmdout(args, res)
    else:
        print "Operation not implemented: {}".format(args.OPERATION)

def vpc_do(cloud, args):
    if args.OPERATION == 'list':
        if args.VPC:
            res = cloud.search_vpcs(args.VPC)
        else:
            res = cloud.list_vpcs()
        print cmdout(args, res)
    else:
        print "Operation not implemented: {}".format(args.OPERATION)

def listener_do(cloud, args):
    if args.OPERATION == 'list':
        if args.LISTENER:
            res = cloud.search_listeners(args.LISTENER)
        else:
            res = cloud.list_listeners()
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
ap_listener = sp.add_parser('listener', help="Elastic Load Balancer Listener")

ap_vpc.add_argument('OPERATION', **crud_operations)
ap_vpc.add_argument('VPC', nargs='?', help="OTC vpc name or id")
ap_elb.add_argument('OPERATION', **crud_operations)
ap_elb.add_argument('ELB', nargs='?', help="OTC elb name or id")
ap_listener.add_argument('OPERATION', **crud_operations)
ap_listener.add_argument('LISTENER', nargs='?', help="OTC elb listener name or id")

ap_vpc.set_defaults(apicmd=vpc_do)
ap_elb.set_defaults(apicmd=elb_do)
ap_listener.set_defaults(apicmd=listener_do)

if __name__ == '__main__':
    args = ap.parse_args()

    cloud = otc.OtcCloud(cloud=args.CLOUD)
    args.apicmd(cloud, args)

# vim: sts=4 ts=4 sw=4 et:
