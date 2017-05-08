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


def testPrint(l):
    print 'hello'

    print dir(l.contents)
    l.contents.value = 13
    return 12

def SendMessage(m):
    d = getListFromMessage(m)
    serPort.write(bytearray(d))



def testReci():
    m = getMessageFromList([55,66,48])
    return m


testP = CFUNCTYPE(c_int,POINTER(c_int))
_testP = testP(testPrint)

'''
testR = CFUNCTYPE(Message)
_testR = testR(testReci)
'''
def testMessageFromPython(m):
    getListFromMessage(m.contents)


testMType = CFUNCTYPE(None, POINTER(Message) )

testM = testMType(testMessageFromPython)


dll.testFuncPoint(_testP);
dll.testregiestMessage(testM)

#dll.regestFunc(_testP,_testR)sendType = CFUNCTYPE(None,None)

'''
def SendMessage(m):
    d = getListFromMessage(m)
    serPort.write(bytearray(d))

def testReci():
    m = getMessageFromList([55,66,48])
    return m

testReci.restype = POINTER(Message)

sendType = CFUNCTYPE(c_int,Message)
recvType = CFUNCTYPE(c_int,POINTER(Message))
#recvType.restype = Message
_send = sendType(SendMessage)
_recv = recvType(testReci)

dll.testRegiestMessage(_send,_recv)'''












