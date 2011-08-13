#!/usr/bin/env python
# coding: utf-8

import boto.ec2
from boto.ec2.connection import EC2Connection

import sys

class RegionStatus:
    def __init__(self, region, conn):
        self.region = region
        self.conn = conn
        self.status = []

    def appendState(self, state):
        self.status.append(state)

    def region(self):
        return self.region

    def connection(self):
        return self.conn

    def regionName(self):
        return self.region.name

    def regionStatus(self):
        return self.status


class AwsStatus:
    """ class to get AWS Status in each region."""

    def __init__(self, ownerId):
        self.ownerId = ownerId
        self.regionStatus = []

    # public
    def connectAllRegions(self):
        regions = boto.ec2.regions()
        for region in regions:
            rs = RegionStatus(region, region.connect())
            self.regionStatus.append(rs)


    # public
    def getStatusOfAllRegions(self):
        for rs in self.regionStatus:

            # get EC2 instances
            for reservation in rs.connection().get_all_instances():
                if reservation.owner_id == self.ownerId:
                    for instance in reservation.instances:
                        rs.appendState({'name':'instance', 'value': [instance.id, instance.key_name, instance.state]})

            # get AMIs
            for image in rs.connection().get_all_images():
                if image.owner_id == self.ownerId:
                    rs.appendState({'name':'image', 'value': [image.id, image.state]})

            # get ELBs
            for volume in rs.connection().get_all_volumes():
                rs.appendState({'name':'volume', 'value': [volume.id, volume.status]})

            # get snapshots
            for snapshot in rs.connection().get_all_snapshots():
                if snapshot.owner_id == self.ownerId:
                    rs.appendState({'name':'snapshot', 'value': [snapshot.id, snapshot.start_time, snapshot.status]})

            # get Elastic IPs
            for address in rs.connection().get_all_addresses():
                if address.instance_id is not None:
                    rs.appendState({'name':'Elastic IP', 'value': [address.public_ip, address.instance_id]})
                else:
                    rs.appendState({'name':'Elastic IP', 'value': [address.public_ip, 'not allocated']})


    # public
    def showStatusOfAllRegions(self):
        ret = ""
        if 0 < len(self.regionStatus):
            for rs in self.regionStatus:
                ret += rs.regionName()
                ret += '\n'
                for status in rs.regionStatus():
                    ret += '\t'
                    ret += status['name']
                    ret += ': '
                    if isinstance(status['value'], list) or isinstance(status['value'], tuple) or isinstance(status['value'], dict):
                        for value in status['value']:
                            ret += value
                            ret += ', '
                    else:
                        ret += status['value']
                    ret += '\n'
        return ret


if __name__ == '__main__':
    ownerId = ''
    if len(sys.argv) > 1:
        ownerId = sys.argv[1]

    print 'now getting data...'
    awsStatus = AwsStatus(ownerId)
    awsStatus.connectAllRegions()
    awsStatus.getStatusOfAllRegions()
    print '---------------------'
    print awsStatus.showStatusOfAllRegions()
