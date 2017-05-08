from ctypes import *

dllPath = "/Users/rainpoll/Desktop/hexBurner/mega1280Protect.dylib"

dll = CDLL(dllPath)

print dllPath




import serial



def getListFromMessage(message):
    x = [];
    for i in range(0, message.size, 1):
        x.append(message.data[i])
    return x;


'''
    this can turn ordinary list to special list like c_byte and represent data type of char From c
    '''
def getMessageFromList(l):
    return Message((c_ubyte *len(l))(*l),c_uint(len(l)))

'''
like structure From c
POINTER(c_ubyte)  likes c code char *
'''
class Message (Structure):
    _fields_= [('data',POINTER(c_ubyte)),
               ('size',c_uint)]


class MegaBurner():

    def __init__(self):
        self.data = ''
        print "start ....."

    def startBurner(self):
        dll.sign_on.restype = Message
        m = dll.sign_on()
        dll.printMessage(m)
        
        return getListFromMessage(m)

    def enterIsporgram(self):
        
        dll.messageFormatByMessage.restype = Message
        dll.cmd_enter_progmode_isp.restype = Message
        
        m = getMessageFromList([0x10,0xc8, 0x64, 0x19, 0x20, 0x00, 0x53, 0x03, 0xac, 0x53, 0x00, 0x00])
        #m = dll.messageFormatByMessage(m)

        n = dll.cmd_enter_progmode_isp(0xc8, 0x64, 0x19, 0x20, 0x00, 0x53, 0x03, 0xac, 0x53, 0x00, 0x00)
       
       
        #     m = dll.messageFormatByMessage(0xc8, 0x64, 0x19, 0x20, 0x00, 0x53, 0x03, 0xac, 0x53, 0x00, 0x00)
        dll.printMessage(n)
        return getListFromMessage(n)

    def get_signature_byte(self,l = [0x30,0,0,0]):

        dll.messageFormatByMessage.restype = Message
        dll.spi_multi.restype = Message
        d = getMessageFromList(l)
        m = dll.spi_multi(0x04,d,0)
        dll.printMessage(m)
        
        return getListFromMessage(m)

    def load_address(self,add = 0x80000000):
        dll.load_address.restype = Message
        dll.messageFormatByMessage.restype = Message
        m =dll.load_address(c_uint(add))


        dll.printMessage(m)

        return getListFromMessage(m)


    def cmd_program_flash_isp(self,d):

        dll.cmd_program_flash_isp.restype = Message
        
        n = getMessageFromList(d)
        
        bh = (len(d)>>8) & 0x00ff
        bl = len(d) & 0x00ff
        
        m = dll.cmd_program_flash_isp(c_ubyte(bh),c_ubyte(bl),0xc1,0x0a,0x40,0x4c,0x20,0,0,n)
        
        dll.printMessage(m)
        
        return getListFromMessage(m)


    def cmd_leave_program_isp(self,pre_t = 0x01,pos_t = 0x01):
        dll.cmd_leave_progmode_isp.restype = Message
        m = dll.cmd_leave_progmode_isp(pre_t,pos_t)
        dll.printMessage(m)
        return getListFromMessage(m)

    def read_flash(self,l):
        dll.messageFormatByMessage.restype = Message
        l = getMessageFromList(l)
        m = dll.messageFormatByMessage(l)
        return getListFromMessage(m)







def hexshow(c):
    l = []
    if len(c)<= 0 :
        print "no recv data"
        return
    for i in range(0,len(c)):
        l.append(ord( c[i:i+1] ))
    
    print 'recv hex----->'
    print l
    return l



def sendData(serPort,d):
    
    size = 0
    index = 0
    data = []
    
    serPort.write(bytearray(d))

    c = bytearray(serPort.read())
    
    if len(c)>0:
        if c[0]==0x1b:
            print 'find 0x1b'
            i =  bytearray(serPort.read())
            j = bytearray(serPort.read())
            
            size = bytearray(serPort.read())[0]
            index = i[0] + j[0]*256
            print 'i = %d, j = %d ,index =%d size = %d'%(i[0],j[0],index,size)
            
            if bytearray(serPort.read())[0] == 0x0e:
                data = bytearray(serPort.read(size+1))
                
    hexshow(data)
    return data

def testData(c):
    if len(c)>0:
        if c[0]==0x1b:
            print 'find test'
            i =  bytearray(serPort.read())
            j = bytearray(serPort.read())
            
            size = bytearray(serPort.read())[0]
            index = i[0] + j[0]*256
            print 'i = %d, j = %d ,index =%d size = %d'%(i[0],j[0],index,size)
            
            if bytearray(serPort.read())[0] == 0x0e:
                data = bytearray(serPort.read(size+1))
                print data
                
                return data
    return None

def gethexFromFile(file):
    fp = open(file)

    xl = []
    for line in fp:
    
        hl = line[9:len(line)-4]
        tl = []
        for i in range(0,len(hl),2):
            m = int(hl[i:i+2],16)
            tl.append(m)
        xl.append(tl)

    print xl[0]
    return xl

def listforhex(l):
    x =[]
    for i in range(0,len(l) - 1,1):
        x+= l[i]

    endhex = []
    for i in range(0,32,1):
        endhex.append( 0xff)
    x+=endhex
    return x


hex = listforhex(gethexFromFile('Blink.ino.hex'))

'''
def testPrint(l):
    print 'hello'
    print l
    return 13


testP = CFUNCTYPE(c_int,c_int)

_testP = testP(testPrint)

dll.testFuncPoint(_testP)

'''

'''
   01 -14
   
   
   10 c8 64 19 20 00 53 03 ac 53 00 00  ---31  CMD_ENTER_PROGMODE_ISP
'''
'''
   1d 04 04 00 30 00 00 00 - 33  spi_muti
   1d 04 04 00 30 00 01 00 - 35
   1d 04 04 00 30 00 02 00 - 37
   
   06 80 00 00 00 - 90    CMD_LOAD_ADDRESS
   13 01 00 c1 0a 40 4c 20 00 00 71 -90  CMD_PROGRAM_FLASH_ISP   1b 07
   
   06 80 00 00 80 -1e   08
   13 01 00 c1 0a 40 4c 20 00 00 09
   
   06 80 00 01 00 -9d    0a
   
   13 01 00 c1 0a 40 4c 20 00 00 84  0b
   
   
   
   
   
   
   
   
   06 80 00 00 00 -9a     1b 0c
   
   14 01 00 20 -29       1b 0d    CMD_READ_FLASH_ISP
   06 80 00 00 80 -18     1b 0e
   
   14 01 00 20 - 2b      1b 0f
   
   06 08 00 01 00 - 87    1b 10
   
   14 01 00 20 -35   1b 11
   
   11 01 01 -15   1b 12    LEAVE_PROGMODE_ISP
   
   
   
   
'''
'''
defind args or returns data type
'''
#dll.testarr.restype = c_char_list
dll.testarr.restype = POINTER(c_ubyte)

dll.test.argtype = Message
dll.test.restype = POINTER(c_ubyte)

'''
using function
'''
'''
message = getMessageFromList([1,2,3])
re = dll.test(message)
dll.printMessage(message)
print getListFromMessage(message)
getListFromMessage(message)
'''


from testSerial import *
import time



port = findPort()
print port
serPort = serial.Serial(port, 115200, timeout=0.2)

m = MegaBurner()
d = m.startBurner()
while 1:
    x = sendData(serPort,bytearray(d))
    t = str(x)

    print t

    if  t.find('AVRISP_2') > 0:
        print 'successed'
        break

d = m.enterIsporgram()
#d = [0x1b, 0x02,0x00 ,0x0c ,0x0e,0x10 ,0xc8 ,0x64 ,0x19 ,0x20 ,0x00 ,0x53 ,0x03 ,0xac ,0x53 ,0x00 ,0x00 ,0x4e]
#d = m.get_signature_byte([0x10 ,0xc8 ,0x64 ,0x19 ,0x20 ,0x00 ,0x53 ,0x03 ,0xac ,0x53 ,0x00 ,0x00])

print d
'''
serPort.write(bytearray(d))
x = bytearray( serPort.read())
'''
x = sendData(serPort,d)

hexshow(x)

'''
serPort.write(bytearray(d))
y = bytearray( serPort.read())
print y[0]
'''

n = m.get_signature_byte([0x30,0,0,0])

x = sendData(serPort,n)



n = m.get_signature_byte([0x30,0x00,0x01,0x00])
x = sendData(serPort,n)



n = m.get_signature_byte([0x30,0,2,0])
x = sendData(serPort,n)



n = m.load_address()
x = sendData(serPort,n)


n = m.load_address(0x80000000)

sendData(serPort, n)

sendData(serPort,m.read_flash([14, 00, 10, 20]))


addr = 0x80000000
addrD = 0
lhex = []

for i in  range(0,len(hex),256):
    
    if (len(hex)-i) < 256:
        lhex = hex[i:]
        for i in range(0,256 -(len(hex)-i)):
            lhex.append(0xff)

    else:
        lhex = hex[i:i+256]
    addr += addrD
    addrD = 256
    
    n = m.load_address(addr)
    sendData(serPort,n)
    
    
    n = m.cmd_program_flash_isp(lhex)
    x = sendData(serPort,n)
'''
for index in range(0,len(hex),256):
    
    lhex = hex[index]
    if index == len(hex) - 1 :
        lhex = endhex
    
 
    addr += addrD
    addrD = len(lhex)
    
    n = m.load_address(addr)
    sendData(serPort,n)

    
    n = m.cmd_program_flash_isp(lhex)
    x = sendData(serPort,n)

print '------------------->>>>>\r\n't
'''

n = m.load_address(0x80000000)

sendData(serPort, n)

sendData(serPort,m.read_flash([14, 00, 10, 20]))

n = m.cmd_leave_program_isp()

sendData(serPort,n)





#function aryEnum(){
#    var result = [];
#        for(var i =0 ; i < ary.length ; i++){
#            var a = ary[i];
#            if( a.next != null ){
#                var n = a.enumID();
#                for(var j = 0; j < n.length ; j++ ){
#                    result.push(n[j]);
#            }
#            }else{
#                result.push( a.id );
#    }
#        }
#        return result;
#}
#
#









'''
n = m.startBurner()

serPort.write(bytearray(n))

for i in range(0,3):
    byte = bytearray(serPort.read())
    
    if byte[0] == 0x1b:
        
        print 'start'
byte = bytearray(serPort.read())
size = byte[0]

byte = bytearray(serPort.read())
if byte[0] == 0x0e:
    print 'flag find'

byte = bytearray(serPort.read(size))
print byte[0]


n = m.enterIsporgram()
b = bytearray(n)
#b += bytearray(n)

print b

serPort.write(b)
c = bytearray(serPort.read())

print len(c)
'''
'''
n = m.get_signature_byte([0x30,0,0,0])

n = m.get_signature_byte([0x30,0,1,0])

n = m.get_signature_byte([0x30,0,2,0])

n = m.load_address()

n = m.cmd_program_flash_isp([])

n = m.cmd_leave_program_isp()

fp = open('test.hex')

xl = []
for line in fp:
    
    hl = line[9:len(line)-4]
    tl = []
    for i in range(0,len(hl),2):
        m = int(hl[i:i+2],16)
        tl.append(m)
    xl.append(tl)

print xl[0]
'''

'''
:100000000C9434000C9446000C9446000C9446006A
0C9434000C9446000C9446000C9446006A


serPort.write(bytes(n))
serPort.readline()
'''
    















