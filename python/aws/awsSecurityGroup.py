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

   def getConnection(self):
       if self.con is not None:
           return self.con
       regions = boto.ec2.regions()
       for region in regions:
           if region.name == self.regionname:
               self.con = region.connect()
               break
       return self.con

   def getGlobalIp(self):
       globalIp = urllib2.urlopen('http://ipcheck.ieserver.net').read()
       print 'Your global IP is ' + globalIp
       return globalIp

   def setIpForSsh(self, mySecurityGroup):
       con = self.getConnection()
       securityGroups = con.get_all_security_groups()
       for sg in securityGroups:
           if sg.name == mySecurityGroup:
               myIp = self.getGlobalIp()
               return sg.authorize('tcp', 22, 22, myIp + '/32')

if __name__ == '__main__':
   ownerId = ''
   regionName = ''
   securityGroupName = ''

   if len(sys.argv) > 1:
       ownerId = sys.argv[1]
   if len(sys.argv) > 2:
       regionName = sys.argv[2]
   if len(sys.argv) > 3:
       securityGroupName = sys.argv[3]

   print 'now setting your Global IP for SSH...'
   securityGroup = AwsSecurityGroup(ownerId, regionName)
   res = securityGroup.setIpForSsh(securityGroupName)
   if res == True:
       print 'Success!'
   else:
       print 'Sorry, error occured..'
