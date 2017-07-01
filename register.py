#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import re
import hashlib

_id = 0

class RegisteUser():
    global _id
#    name = ""
#    email = ""
#    password = ""
#    id = _id
#
#    now = datetime.datetime.now()
#    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    def __init__(self,name,email,password,timestamp,headImg):
        global _id
        self.id = _id
        self.name = name
        self.password = ""
        self.email = ""
        self.timestamp = ""
        
        e = re.match(r'^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$',email)
        if e:
            self.email = e.group()
        else:
            print 'email error'
        
        if len(password)>6:
            self.password = password
        else :
            print "password too short please enter 8"
        
        
        if len(timestamp)>10:
            self.timestamp = timestamp
        else:
            now = datetime.datetime.now() + datetime.timedelta(hours=8)
            self.timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        self.headImg =headImg
    ls
        _id += 1


class XyEncode():

    def md5(self,str):
        import hashlib
        import types
        if type(str) is types.StringType:
            m = hashlib.md5()
            m.update(str)
            return m.hexdigest()
        else:
            return ''

    def base64Encode(self,str):
        import base64
        import types
        if type(str) is types.StringType:
            return base64.b64encode(str)
        else:
            return ''

    def base64Decode(self,str):
        import base64
        import types
        if type(str) is types.StringType:
            return base64.b64decode(str)
        else:
            return ''

    def sha1(self,str):
        import hashlib
        import types
        if type(str) is types.StringType:
            hash = hashlib.sha1()
            hash.update(str.encode('utf-8'))
            return hash.hexdigest()
        else:
            return ''




if __name__ == '__main__':
    r = RegisteUser('test','1091976750@qq.com','123456','2017-02-21 02:03:17')
    print  r.id
    print  r.password
    print  r.email
    print  r.timestamp
    
    r = RegisteUser('test2','-1091976750@qq.com','123456789','2017-02-21 02:03:17')
    print  r.id
    print  r.email
    print  r.password
    print  r.timestamp
    
    
    t = 'raind5fsdfdsfjasfjdkafjalfjdsalkfjdlakfjsdkfjdsfjdslkfjdskfjaljfdkfjsdlkfjd'
    
    print XyEncode().sha1(t)
    print XyEncode().md5('fdfd')
    b = XyEncode().base64Encode(t)
    print b
    print XyEncode().base64Decode(b)

