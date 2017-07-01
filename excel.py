#!coding=utf-8
#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Created by Rain on 17/3/1.
#  Copyright © 2017年 Rain. All rights reserved.
#
#  http://192.168.1.63/IBOS/?r=user/default/login

#import urllib,urllib2
#url='http://192.168.1.63/IBOS/?r=user/default/login/'
#textmod ={'user':'admin','password':'123456','loginsubmit':'1'}
#textmod = urllib.urlencode(textmod)
#print(textmod)
##输出内容:password=admin&user=admin
#req = urllib2.Request(url = '%s%s%s' % (url,'?',textmod))
#req = urllib2.Request(url)
#res = urllib2.urlopen(req)
#res = res.read()
#print(res)
##输出内容:登录成功

import  xdrlib ,sys
import xlrd
import urllib,urllib2
import json

def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= '/Users/rainpoll/Desktop/母婴-2017-05-26.xls',colnameindex=0,by_index=-1):
    print "file path: %s"%(file)
    data = open_excel(file)
    sheets = data.sheets();
    if  len(sheets)>0:
        pass
    else:
        print 'there is no any sheet in excel'
        return;
    if by_index > -1:
        sheets = data.sheets()[by_index];
    for table in sheets:
#        table = sheets[index]
        nrows = table.nrows #行数
        ncols = table.ncols #列数'
        
        print "excel行数:%d 列数:%d"%(nrows ,ncols)
        colnames =  table.row_values(colnameindex) #某一行数据
        list =[]
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
    return list


def updateByGet(url='http://127.0.0.1:8000/home'):

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

def updateByPost(url='http://127.0.0.1:8000/home/',params1 = {}):
    params = json.dumps(params1)
    res = urllib.urlopen(url,(params))
    print res.read()

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= '/Users/rainpoll/Desktop/母婴-2017-05-26.xls',colnameindex=0,by_name=u'Page1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
                list.append(app)
    return list

def main():
    tables = excel_table_byindex()
#    for row in tables:
#        print row
#    tables = excel_table_byname()
#    for row in tables:
#        print row

#    testGet()
    tempData = [{
                "id":0,
                'str':"this is good"
                }]
                
    updateByPost('http://127.0.0.1:8000/home/',tempData);



def testAutoExcel(file= '/Users/rainpoll/Desktop/母婴-2017-05-26.xls',colnameindex=0,by_name=u'Page1'):
    line_0 = "line_0"
    line_1 = "line_1"
    
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)

        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
                list.append(app)

    return list

def getParm():
    parm = sys.argv

    if len(parm) and parm[1]:





def processArg():

    import sys
    import os.path
    import time
    startArg = 1
    if len(sys.argv) <= 1:
        help();
        return;
    
    for i in range(startArg, len(sys.argv)):
        path = sys.argv[i]
        if os.path.exists(path):
            print 'progress excel file...'
            time.sleep(1)
            tables = excel_table_byindex(path)
            time.sleep(1)
            print 'progress excel file sucess'
            
            print "start update ..."
            time.sleep(1)
            updateByPost('http://127.0.0.1:8000/home/',tables);
            print "updtate done"
        else:
            print "\nerror!! path is not exist\n"



def help():
    print "参数为excel路径,多个参数用命令行隔开"
    sys.exit(10);

if __name__ == '__main__':
    # main()
    processArg()



''' 
{u'淘宝客短链接(300天内有效)': u'https://s.click.taobao.com/77dfVkw', u'是否为营销计划商品': u'否', u'淘口令(300天内有效)': u'￥B8QRtyXlkv￥', u'优惠券链接': u'https://uland.taobao.com/coupon/edetail?e=koFxYQ6faEwN%2BoQUE6FNzJxKx1Vx91ARJL5ncMMNymOL%2Bx4Xcu%2BaPvshiv4bllT5TpKEW2QUdg9FljfOv45NDwPbfjxGQb3QoUC34ijeiBuTeFKmpJx14IFKnXO9XPFOgO8xj2oU5z1WN1b9Z1xNT5NvJDNcA99Q&pid=mm_118694617_20714278_70210785&af=1', u'淘宝客链接': u'https://s.click.taobao.com/t?e=m%3D2%26s%3DRH4Cqq7dlrQcQipKwQzePOeEDrYVVa64K7Vc7tFgwiHjf2vlNIV67jbeHkLJm9oR2VSL3ITNpk0x8fHh%2FjmheCUXc5sD0wcZaLjpOdAH9T1edEib0MaaeShKEquordj0Oxtul%2BqfVr4lXEXv2FFRtgctV4LAZ5Ttxg5p7bh%2BFbQ%3D&pvid=11_42.120.75.2_419_1495767044854', u'商品名称': u'米宝兔音乐脚踏钢琴健身架宝宝健身器3-12个月新生婴儿玩具0-1岁', u'商品月销量': u'6504', u'收入比率(%)': u'5.60', u'优惠券短链接(300天内有效)': u'https://s.click.taobao.com/JwgfVkw', u'商品主图': u'http://img.alicdn.com/bao/uploaded/i1/TB14UQAOFXXXXXuapXXXXXXXXXX_!!0-item_pic.jpg', u'商品价格(单位：元)': u'168.00', u'卖家旺旺': u'米宝兔垂直专卖店', u'商品id': u'45529296801', u'优惠券淘口令(300天内有效)': u'￥bnqWtyXkyD￥', u'商品详情页链接地址': u'http://item.taobao.com/item.htm?id=45529296801', u'佣金': u'9.41', u'店铺名称': u'米宝兔垂直专卖店', u'优惠券剩余量': u'7645', u'优惠券开始时间': u'2017-04-30', u'优惠券总量': u'20000', u'优惠券面额': u'满99元减5元', u'优惠券结束时间': u'2017-05-31'}
'''

'''
{u'淘宝客短链接(300天内有效)': u'https://s.click.taobao.com/K9gfVkw', u'是否为营销计划商品': u'是', u'淘口令(300天内有效)': u'￥5exMtyX79k￥', u'优惠券链接': u'https://uland.taobao.com/coupon/edetail?e=mIVasQQFH%2BMN%2BoQUE6FNzJxKx1Vx91ARJL5ncMMNymOL%2Bx4Xcu%2BaPvshiv4bllT5OwNyX8AnKU2Fn98KnSh7o0YUejVMpzGc7sRUcQe1PUdpOxmrRmuElDLA%2BaCCpuNG1A3fML1f5zlryLi6zrP2eplFpAgXpf0Jonv6QcvcARY%3D&pid=mm_118694617_20714278_70210785&af=1', u'淘宝客链接': u'https://s.click.taobao.com/t?e=m%3D2%26s%3Dkp%2BVZeppnbYcQipKwQzePOeEDrYVVa64K7Vc7tFgwiHjf2vlNIV67jbeHkLJm9oRJ%2BAVY%2F4wKC0x8fHh%2FjmheCUXc5sD0wcZaLjpOdAH9T1edEib0MaaeTXMQ%2F1t%2BbWWvZLFKRjLMprrH9qPUYCKxNUI7OtokbapV0qK0WHZHYSiZ%2BQMlGz6FQ%3D%3D&pvid=11_42.120.75.2_419_1495767044854', u'商品名称': u'女童皮鞋公主鞋真皮2017春秋新款女孩儿童单鞋学生黑色演出女童鞋', u'商品月销量': u'601', u'收入比率(%)': u'30.50', u'优惠券短链接(300天内有效)': u'https://s.click.taobao.com/XElfVkw', u'商品主图': u'http://img.alicdn.com/bao/uploaded/i1/TB1XFyyRXXXXXbHaXXXXXXXXXXX_!!0-item_pic.jpg', u'商品价格(单位：元)': u'79.00', u'卖家旺旺': u'奔仔鼎尚专卖店', u'商品id': u'520734129887', u'优惠券淘口令(300天内有效)': u'￥XpgetyXSJL￥', u'商品详情页链接地址': u'http://item.taobao.com/item.htm?id=520734129887', u'佣金': u'24.10', u'店铺名称': u'奔仔鼎尚专卖店', u'优惠券剩余量': u'958', u'优惠券开始时间': u'2017-05-24', u'优惠券总量': u'1000', u'优惠券面额': u'满79元减40元', u'优惠券结束时间': u'2017-05-31'} 
'''
