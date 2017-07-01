#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
#  Created by Rain on 17/3/1.
#  Copyright © 2017年 Rain. All rights reserved.
#

import os, sys, stat

# Assuming /tmp/foo.txt exists, Set a file execute by the group.
## Set a file write by others.
#os.chmod("/tmp/foo.txt", stat.S_IWOTH)
#print "Changed mode successfully!!"
#This produces following result:
#Changed mode successfully!!
#os.chmod("/tmp/foo.txt", stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH) # mode:777

#stat.S_ISUID: Set user ID on execution.
#stat.S_ISGID: Set group ID on execution.
#stat.S_ENFMT: Record locking enforced.
#stat.S_ISVTX: Save text image after execution.
#stat.S_IREAD: Read by owner.
#stat.S_IWRITE: Write by owner.
#stat.S_IEXEC: Execute by owner.
#stat.S_IRWXU: Read, write, and execute by owner.
#stat.S_IRUSR: Read by owner.
#stat.S_IWUSR: Write by owner.
#stat.S_IXUSR: Execute by owner.
#stat.S_IRWXG: Read, write, and execute by group.
#stat.S_IRGRP: Read by group.
#stat.S_IWGRP: Write by group.
#stat.S_IXGRP: Execute by group.
#stat.S_IRWXO: Read, write, and execute by others.
#stat.S_IROTH: Read by others.
#stat.S_IWOTH: Write by others.
#stat.S_IXOTH: Execute by others.
import sys
import os.path

filed = 0;
success = 0;
cmd = stat.S_IRUSR

def dirProgress(rootdir):
#    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
#    print list
#    for i in range(0,len(list)):
#        path = os.path.join(rootdir,list[i])
#        print path
#        if os.path.isfile(path):
#            print "path ---",path
#
    global filed
    global success
    for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
 #            print "parent :  ",parent
#            print "filename :  ",filename
            path = os.path.join(parent,filename)
            print "full file name of file is : ",path

            if os.path.exists(path):
                t = os.chmod(path, cmd)
#            print "success :",path," change attribute OK !"
                success += 1
            else:
                print "error : file \"" + path +"\" not found, please check this direction"
                filed += 1;

def main_old():

    global filed
    global success
    global cmd
    startArg = 1;
    excuteDirection = False;
    #    print 'filename---' + sys.argv[0]
    print 'sys.argv ---',len(sys.argv),sys.argv[0]
    
    if len(sys.argv) <= 1:
        help();
        return

    if "-wr" in sys.argv:
        cmd = stat.S_IRWXU
        startArg += 1;
    
    if "-r" in sys.argv:
        cmd = stat.S_IREAD
        startArg += 1;

    if "-w" in sys.argv:
        cmd = stat.S_IWRITE
        startArg += 1;

    if "-a" in sys.argv:
        startArg += 1;
        excuteDirection = True;

    if "-f" in sys.argv:
        startArg += 1;
        excuteDirection = False;

    if "-help" in sys.argv:
        help();
        return

    for i in range(startArg, len(sys.argv)):
        path = sys.argv[i]
        
        if(excuteDirection):
            if os.path.isdir(path):
                dirProgress(path);
        else:
            if os.path.exists(path):
                t = os.chmod(path, cmd)
#            print "success :",path," change attribute OK !"
                success += 1
            else:
                print "error : file \"" + path +"\" not found, please check this direction"
                filed += 1;
    print "warning :","success[",success,"]", "  failed : [",filed,"]"
    if filed > 1000:
        print "too many filed";
        return sys.exit(-1);
    result = 100*100 + filed % 10+1;
    print result
    return  sys.exit(result);

def help():
    print "命令行参数 :"
    print "参数arg[1] 可选: -wr :文件设置本用户可读可写" + "  -w :文件设置本用户只写" + " -r :文件设置本用户只读(缺省项)"
    print "参数arg[2] 可选: -a :修改文件目录下所有文件" + " -f :修改指定文件或者路径(缺省项)"
    print "参数arg[3] 必选: 文件目录/路径"
    sys.exit(10);


#def processExcel:
# -*- coding: utf-8 -*-
import  xdrlib ,sys
import xlrd
def open_excel(file= 'file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= '/Users/rainpoll/Desktop/母婴-2017-05-26.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
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

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= '/Users/rainpoll/Desktop/母婴-2017-05-26.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row is not:
       		app = {}
         	for i in range(len(colnames)):
                        app[colnames[i]] = row[i]
                        list.append(app)
    return list

def main():
    tables = excel_table_byindex()
    for row in tables:
            print row
                
    tables = excel_table_byname()
    for row in tables:
    print row



if __name__ == '__main__':
    main()

