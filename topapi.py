# -*- coding: utf-8 -*-
import top.api


req=top.api.TbkItemGetRequest(url,port)
req.set_app_info(top.appinfo(appkey,secret))

req.fields="ti"
req.q="女装"
try:
    resp= req.getResponse()
    print(resp)
except Exception,e:
    print(e)
