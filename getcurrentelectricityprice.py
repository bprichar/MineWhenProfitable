#!/usr/bin/env python

import json
import urllib2
from datetime import datetime, timedelta

def getCurrentPrice():
    baseaddress = 'https://rrtp.comed.com/api?type=5minutefeed&datestart='
    starttime = datetime.strftime(datetime.now() - timedelta(minutes=10), '%Y%m%d%H%M')
    endtime = datetime.strftime(datetime.now(), '%Y%m%d%H%M')
    address = baseaddress + starttime + '&dateend=' + endtime
    return json.loads(urllib2.urlopen(address).read())[-1]['price']

print getCurrentPrice()

