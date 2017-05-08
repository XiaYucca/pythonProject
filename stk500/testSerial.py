# -*- encoding: utf-8 -*-


import serial,struct
#import codecs

#if __name__ == '__main__':
#    import inkex
# import argparse

def version():
    return "0.1"  # Version number for this document


def findPort():
    # Find a single EiBotBoard connected to a USB port.
    print("start find port")
    try:
        from serial.tools.list_ports import comports
    except ImportError:
        comports = None
        return None
    if comports:
        comPortsList = list(comports())

        print(comPortsList)
        EBBport = None
        for port in comPortsList:
            #			help(port.usb_info)
            #			print(port.usb_info)
            print(port[0])
            print(port[1])
            print(port[2])
            if port[1].startswith("Arduino"):
                EBBport = port[0]  #Success; EBB found by name match.
                print('Success; Anduino found by name matc%s' %(EBBport))
                break  #stop searching-- we are done.
        if EBBport is None:
            for port in comPortsList:
                if port[2].startswith("USB VID:PID=2341:0042"):
                    EBBport = port[0]  #Success; EBB found by VID/PID match.
                    print('#Success; Arduino found by VID/PID match.')
                    break  #stop searching-- we are done.
        return EBBport


def testPort(comPort):
    '''
	Return a SerialPort object
	for the first port with an EBB (EiBotBoard; EggBot controller board).
	YOU are responsible for closing this serial port!
	'''
    if comPort is not None:
        try:
            serialPort = serial.Serial(comPort, timeout=1.0)  # 1 second timeout!
            serialPort.write('v\r')
            strVersion = serialPort.readline()
            if strVersion and strVersion.startswith('EBB'):
                return serialPort

            serialPort.write('v\r')
            strVersion = serialPort.readline()
            if strVersion and strVersion.startswith('EBB'):
                return serialPort
            serialPort.close()
        except serial.SerialException:
            pass
        return None
    else:
        return None


def openPort():
    foundPort = findPort()
    serialPort = testPort(foundPort)
    if serialPort:
        return serialPort
    return None


def closePort(comPort):
    if comPort is not None:
        try:
            comPort.close()
        except serial.SerialException:
            pass


def query(comPort, cmd):
    if (comPort is not None) and (cmd is not None):
        response = ''
        try:
            comPort.write(cmd)
            response = comPort.readline()
            unused_response = comPort.readline()  # read in extra blank/OK line
        except:
            inkex.errormsg(gettext.gettext("Error reading serial data."))
        return response
    else:
        return None


def command(comPort, cmd):
#    print "command"
    if (comPort is not None) and (cmd is not None):
        try:
            comPort.write(cmd)
            response = comPort.readline()
            print(response)
            if ( response != 'OK\r\n' ):
                if ( response != '' ):
                    inkex.errormsg('After command ' + cmd + ',')
                    inkex.errormsg('Received bad response from EBB: ' + str(response) + '.')
                else:
                    inkex.errormsg(gettext.gettext('EBB Serial Timeout.'))
        except:
            pass


def send(port, cmd):

    commandtest(port, cmd)
    
def testSend():
    import fileinput
    ctx = """
G90
G21
G0 X26.1159 Y5.2533

G4 P0.3
M03 S60
G4 P0.3

G1F4000
G02 X26.3186 Y5.8116 I469.3198 J-170.1034
G02 X29.675 Y15.0367 I132312.0141 J-48132.5342
G03 X33.0272 Y24.2625 I-10030.8704 J3649.9621
G01 X33.0317 Y24.2882
G01 X33.0185 Y24.3014
G03 X28.4373 Y24.3146 I-4.5813 J-796.9542
G02 X23.8969 Y24.3521 I-0. J274.8315
G01 X23.8711 Y24.3901
G00 x0 y0
"""
    filePath = "/Users/rainpoll/Desktop/LOGOZUIZONG.nc"
    
    port = findPort()
    serPort = serial.Serial(port, 115200, timeout=3.0)
    serPort.write('test send')

    file = open(filePath)
    
    for line in file :
        send(serPort,line)
 #       print line
 #       send(serPort,line)
    
def testProgram(cmd) :
    port = findPort()
    serPort = serial.Serial(port, 115200, timeout=1.0)

    for temp in cmd :
        serPort.write(cmd)

    print(serPort.readline())



def commandtest(comPort, cmd):
#    print "command"
    if (comPort is not None) and (cmd is not None):
        try:
            comPort.write(cmd)
            response = comPort.readline()
            print(response)
            if ( response != 'OK\r\n' ):
                if ( response != '' ):
                    inkex.errormsg('After command ' + cmd + ',')
                    inkex.errormsg('Received bad response from EBB: ' + str(response) + '.')
                else:
                    inkex.errormsg(gettext.gettext('EBB Serial Timeout.'))
        except:
            pass


def fileTransion3(path):
    import fileinput
    import time

    port = findPort()
    serPort = serial.Serial(port, 115200, timeout=3.0)

    file = open(path);

    rev = 'ok'
  #  serPort.write(bytes("$$", encoding="utf8"))
 #   print(serPort.readline())

 #   serPort.write(bytes("$$", encoding="utf8"))
 #   print(serPort.readline())
#    for j in range(1, 40):
#        serPort.write(bytes("g0 x0 y0", encoding="utf8"))
    print('------------------')
    for line in file:
	#	l = line.decode("utf-8")
        commandtest(serPort, bytes(line,encoding="utf8"))
    closePort(serPort)








def main(path):
    fileTransion3(path)


def ConvertStrData(strData):
    for c in ['gb18030', 'utf-8', 'big-5']:
        try:
            return strData.decode(c).encode("utf-8")
        except:
            continue
    return strData


def sendMessage(serPort, data):
    message = struct.pack(">BBHB", 0x1B, 1, len(data), 0x0E)
    for c in data:
        message += struct.pack(">B", c)
    checksum = 0
    for c in message:
        checksum ^= ord(c)
    message += struct.pack(">B", checksum)
    try:
        serPort.write(message)
        serPort.flush()
    except Serial.SerialTimeoutException:
        raise ispBase.IspError('Serial send timeout')
    #self.seq = (self.seq + 1) & 0xFF
#    return recvMessage()

#__name__ = '__main__'

if __name__ == '__main__':
	pass
'''
print('test open serial')

port = findPort()
print port
serPort = serial.Serial(port, 115200, timeout=1.0)
cmd = [0x30 ,0x20]

item = 0x50

print(type(bytes(item)))





sendMessage(serPort,[0x30,0x20])





for i in range(1,5):
    for temp in cmd :
    #   serPort.write(hex(temp))
        serPort.write(bytes([0x1b,0x01 ,0x00 ,0x01 ,0x0e ,0x01, 0x6b]))
        rev = serPort.readline()
    print(rev)

print (type(rev))





#testSend() '''

