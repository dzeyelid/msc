#!/usr/bin/env python
# coding: utf-8

import boto.ec2
from boto.ec2.connection import EC2Connection
import urllib2
import sys

class AwsSecurityGroup:
    def __init__(self, ownerId, regionname):
        self.ownerId = ownerId
        self.regionname = regionname
        self.con = None

    def get_connection(self):
        if self.con is not None:
            return self.con
        regions = boto.ec2.regions()
        for region in regions:
            if region.name == self.regionname:
                self.con = region.connect()
                break
        return self.con

    def get_global_ip(self):
        globalIp = urllib2.urlopen('http://ipcheck.ieserver.net').read()
        print 'Your global IP is ' + globalIp
        return globalIp

    def set_ip_for_ssh(self, mySecurityGroup, revoke_others=True):
        con = self.get_connection()
        securityGroups = con.get_all_security_groups()
        for sg in securityGroups:
            if sg.name == mySecurityGroup:
                # delete other ssh IP
                for rule in sg.rules:
                    if rule.ip_protocol == 'tcp' and \
                            rule.from_port == '22' and rule.to_port == '22':
                        for grant in rule.grants:
                            if revoke_others == True:
                                print 'revoke ', grant.cidr_ip
                                sg.revoke(ip_protocol='tcp', from_port=22, to_port=22, cidr_ip=grant.cidr_ip)

                # set my global IP
                myIp = self.get_global_ip()
                return sg.authorize('tcp', 22, 22, myIp + '/32')


if __name__ == '__main__':
    ownerId = ''
    regionName = ''
    securityGroupName = ''
    revoke_others = True

    if len(sys.argv) > 1:
        ownerId = sys.argv[1]
    if len(sys.argv) > 2:
        regionName = sys.argv[2]
    if len(sys.argv) > 3:
        securityGroupName = sys.argv[3]
    if len(sys.argv) > 4:
        if sys.argv[4].lower() == 'false':
            revoke_others = False

    print 'now setting your Global IP for SSH...'
    securityGroup = AwsSecurityGroup(ownerId, regionName)
    res = securityGroup.set_ip_for_ssh(securityGroupName, revoke_others)
    if res == True:
        print 'Success!'
    else:
        print 'Sorry, error occured..'
