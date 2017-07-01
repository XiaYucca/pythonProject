#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Created by Rain on 17/3/1.
#  Copyright © 2017年 Rain. All rights reserved.
#
#  http://192.168.1.63/IBOS/?r=user/default/login

import urllib,urllib2
url='http://192.168.1.63/IBOS/?r=user/default/login/'
textmod ={'user':'admin','password':'123456','loginsubmit':'1'}
textmod = urllib.urlencode(textmod)
print(textmod)
#输出内容:password=admin&user=admin
req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
req = urllib2.Request(url)
res = urllib2.urlopen(req)
res = res.read()
print(res)
#输出内容:登录成功
