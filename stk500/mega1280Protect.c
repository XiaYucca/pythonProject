//
//  mega1280Protect.c
//  AlsRobot_4WD
//
//  Created by RainPoll on 16/7/13.
//  Copyright © 2016年 RainPoll. All rights reserved.
//

#include "mega1280Protect.h"
#include <stdlib.h>

#define message_start 0x1B
#define message_mark 0x0E

#define CMD_LOAD_ADDRESS  0x06
#define CMD_ENTER_PROGMODE_ISP 0x10
#define CMD_SPI_MULTI 0x1D
#define CMD_PROGRAM_FLASH_ISP 0x13
#define CMD_LEAVE_PROGRAM_MODE 0x11




unsigned char * messageFormat(unsigned char *data, unsigned int  dataSize)
{
   static unsigned char num = 0;
   unsigned char chack = 0;
   unsigned char h_size;
   unsigned char l_size;
   unsigned char *result;
    
   unsigned int size = dataSize + 6;

    num ++;  //
    
    h_size = (dataSize >> 8)&0xff;
    l_size = dataSize & 0x00ff;
    
    result = malloc((dataSize + 6)*sizeof(unsigned char));
    
    
    printf("process data size%d",size);
    for (int i = 0; i < size; i ++) {
       
        if (i == 0) {
            result[i] = message_start;
        }else if (i == 1)
        {
            result[i]= num;
        }
        else if (i == 2)
        {
            result[i]= h_size;
        }else if(i == 3)
        {
            result[i] = l_size;
        }else if (i == 4)
        {
            result[i]= message_mark;
        }else if (i == dataSize + 5)
        {
            result[i] = chack;
            return result;
            
        }else
        {
            
            result[i] = data[i-5];
        }
        
        chack ^= result[i];

        
    }
    
    return result;
}


Message messageFormatByMessage(Message message)
{
    Message me ={  messageFormat(message.data, message.size), message.size + 6};
    return me;
}

Message messageFormatByList(unsigned char *data,unsigned short dataSize)
{
    Message me ={  messageFormat(data, dataSize), dataSize + 6};
    return me;
}


Message sign_on()
{
    unsigned char CMD_SIGN_ON = 0x01 ;
    
   return messageFormatByList(&CMD_SIGN_ON, 1);
}


Message load_address(unsigned int address)
{
    unsigned char data[4]={0};
    
    data[0] = (address >> 24) & 0xff;
    data[1] = (address >> 16) & 0xff;
    data[2] = (address >> 8) & 0xff;
    data[3] = (address) & 0xff;
    
    
    unsigned char dataM[5] = {CMD_LOAD_ADDRESS,data[0],data[1],data[2],data[3]};
    
    Message me = {dataM , 5};
    return messageFormatByMessage(me);
}


Message send_chip_erase_isp()
{
    unsigned char CMD_CHIP_ERASE_ISP                  = 0x12;
    
    unsigned char data[7] = {CMD_CHIP_ERASE_ISP,0x37,0x00,0xac,0x80,0x00,0x00};
    
    return messageFormatByList(data, 7);
    
}

Message spi_multi(unsigned char numRx,Message data,unsigned char rxStartAddr)
{   unsigned char *dataM;
    dataM = malloc((4 + data.size)* sizeof(unsigned char));
    
    dataM[0] = CMD_SPI_MULTI;
    dataM[1] = data.size;
    dataM[2] = numRx;
    dataM[3] = rxStartAddr;
    
    for (int i = 0; i<data.size; i++) {
        dataM[i+4] = (data.data)[i];
    }
   Message message = {dataM,data.size + 4};
   return messageFormatByMessage(message);
}

Message cmd_enter_progmode_isp(
                            unsigned char timeout,
                            unsigned char stabDelay,
                            unsigned char cmdexeDelay,
                            unsigned char synchLoops,
                            unsigned char byteDelay,
                            unsigned char pollValue,
                            unsigned char pollIndex,
                            unsigned char cmd1,
                            unsigned char cmd2,
                            unsigned char cmd3,
                            unsigned char cmd4)
{
//    unsigned char CMD_ENTER_PROGMODE_ISP ;
//    unsigned char timeout;
//    unsigned char stabDelay;
//    unsigned char cmdexeDelay;
//    unsigned char synchLoops;
//    unsigned char byteDelay;
//    unsigned char pollValue;
//    unsigned char pollIndex;
//    unsigned char cmd1;
//    unsigned char cmd2;
//    unsigned char cmd3;
//    unsigned char cmd4;
    
    unsigned char cmd[12]={CMD_ENTER_PROGMODE_ISP,timeout,stabDelay,cmdexeDelay,synchLoops,byteDelay,pollValue,pollIndex,cmd1,cmd2,cmd3,cmd4};
    
    Message message = { cmd, 12};
    
    return messageFormatByMessage(message);
}


Message cmd_leave_progmode_isp(unsigned char preDelay, unsigned char postDelay)
{
    unsigned char cmd[3] = {CMD_LEAVE_PROGRAM_MODE,preDelay,postDelay};
    
    Message message = {cmd,3};
    
    return messageFormatByMessage(message);
}


Message cmd_chip_erase_isp(unsigned char eraseDelay, unsigned char pollMethod, unsigned char cmd1 ,unsigned char cmd2, unsigned char cmd3, unsigned char cmd4)
{
    unsigned char CMD_CHIP_ERASE_ISP  = 0x12;
    
    unsigned char data[7] = {CMD_CHIP_ERASE_ISP,eraseDelay,pollMethod,cmd1,cmd2,cmd3,cmd4};
    
    return messageFormatByList(data, 7);
}


Message cmd_program_flash_isp(unsigned char numBytes_h,
                              unsigned char numBytes_l,
                              unsigned char mode,
                              unsigned char cmd_delay,
                              unsigned char cmd1,
                              unsigned char cmd2,
                              unsigned char cmd3,
                              unsigned char poll1,
                              unsigned char poll2,
                              Message data )
{
    unsigned char *dataM = malloc((data.size + 10)*sizeof(unsigned char));
    dataM[0] = CMD_PROGRAM_FLASH_ISP;
    dataM[1] =numBytes_h;
    dataM[2] =numBytes_l;
    dataM[3] =mode;
    dataM[4] =cmd_delay;
    dataM[5] =cmd1;
    dataM[6] =cmd2;
    dataM[7] =cmd3;
    dataM[8] = poll1;
    dataM[9] = poll2;
    
    for (int i = 0; i<data.size; i++) {
        dataM[i+10] = data.data[i];
    }
    
    Message message = {dataM,data.size+10};
    return messageFormatByMessage(message);
}

Message write_hfuse(unsigned char byte)
{
    unsigned char bytes = 0xd8;
    if (byte) {
        bytes = byte;
    }
    unsigned char data[4]={0xac,0xa8,0x00,bytes};
    
    Message me = {data ,4};
    
    Message m2 = {{1,2,3,4},4};
    
   return  spi_multi(4, me, 0);
}

Message write_lfuse(unsigned char byte)
{
    unsigned char bytes = 0xef;
    if (byte) {
        bytes = byte;
    }
    unsigned char data[4]={0xac,0xa0,0x00,bytes};
    
    Message me = {data ,4};
    
    Message m2 = {{1,2,3,4},4};
    
    return  spi_multi(4, me, 0);
}

Message write_efuse(unsigned char byte)
{
    unsigned char bytes = 0xff;
    if (byte) {
        bytes = byte;
    }
    unsigned char data[4]={0xac, 0xA4, 0x00, bytes};
    
    Message me = {data ,4};
    
    Message m2 = {{1,2,3,4},4};
    
    return  spi_multi(4, me, 0);
}





void mega_enter_progmode_isp()
{
    printMessage(
                 cmd_enter_progmode_isp(0xc8, 0x64, 0x19, 0x20, 0x00, 0x53, 0x03, 0xac, 0x53, 0, 0)
                 );
}

void mega_chip_erase_isp()
{
    printMessage(
                 cmd_chip_erase_isp(0x37, 0x00, 0xac, 0x80, 0, 0)
                 );
}

void mega_load_page(Message data)
{
    unsigned char numByte_h = data.size >> 8 & 0xff;
    unsigned char numByte_l = data.size & 0x00ff;
    
    printMessage(
                 cmd_program_flash_isp(numByte_h, numByte_l, 0xc1, 0X06, 0X40, 0X4C, 0X20, 0, 0, data)
                 );

}

void mega_load_address(unsigned int addr)
{
    unsigned int address ;
    unsigned char WORDSIZE = 2;
    
    load_address(address / WORDSIZE);
}

float mega_load_data(Message data)
{
    unsigned int currentByteAddr = 0;
    unsigned int size = data.size;
    unsigned int blockSize = 0x0080;
    float progress = 0.0;
    
    while (currentByteAddr < size) {
        
        mega_load_address(currentByteAddr);
        
        Message temp = messageSub(data, currentByteAddr, blockSize);
        
        mega_load_page(temp);
        
        progress = (currentByteAddr)/size;
        
    }
    return  progress;
}




/******************
 测试用的
 *****************/
Message messageSub( Message message, unsigned int  index ,unsigned int length)
{
    unsigned int len = message.size;
    Message rem ;
    
    if (index > len) {
        printf("error out range of message");
        return rem;
    }
    
    if (index + length > len) {
        length = len - index;
    }
    unsigned char * data = malloc(length * sizeof(unsigned char));
    
    for (int i = 0 ; i< length ;i++) {
        data[i] = message.data[index + i];
    }
    rem.data = data;
    rem.size = length;
    
    return rem;
}

Message messageApendMessage(Message m1,Message m2)
{
    unsigned char *temp = malloc((m1.size + m2.size)*sizeof(unsigned char));
    
    for (int i = 0; i < m1.size + m2.size  ; i++) {
        if (i< m1.size) {
            temp[i] = m1.data[i];
        }else
        {
            temp[i] = m2.data[i- m1.size];
        }
    }
    
    Message message = {temp ,m1.size + m2.size};
    return message;
}

Message messageFromString(char* str)
{
    int len = 0;
    char *orStr = str;
    while (*str) {
        len ++;
        str++;
    }
    unsigned char *r = malloc(len * sizeof(unsigned char));
    
    while (*orStr) {
        *(r++) = *(orStr++);
    }
    
    Message message = {r,len};
    return message;
}

Message messageFromArr(char* data,int size)
{
    Message message = {data,size};
    
    return message;
}



int messageContentMessage(Message m1,Message m2)
{
    int  flag = 0;
    int  isFind = 0;
    if (m2.size > m1.size) {
        return 0;
    }
    for(int i = 0; i < m1.size ; i ++)
    {
        for (int j = i; j < m2.size; j++) {
            
            if (m1.data[i] == m2.data[j]) {
                flag ++;
                break;
            }
            else
            {
                flag = 0;
            }
            
        }
        if (flag == m2.size) {
            
            isFind = 1;
            break;
            
        }
        if ( (i > m1.size - m2.size) && (flag == 0) ) {
            break;
        }
        
    }
    return isFind;
}

void printMessage(Message m)
{
    printf("\nmessageSize : %d = (\n",m.size);
    
    for (int i = 0; i < m.size ; i++) {
        printf("%.2x ",m.data[i]);
    }
    printf(")\n");
}




/********************************/

/********************************/

Message test(Message ch)
{
    printf("c_function print\r\n");
    
    printf("c_function arg -data %d\r\n",ch.data[0]);
    
    printf("c_function arg -size %d\r\n",ch.size);
    
    return ch;
}

char *testarr(char *data)
{
 
    printf("testarr_arg \r\n");
    printf("v1 = %d\r\n",data[0]);
    printf("v2 = %d\r\n",data[1]);
    return data;
}

void testFuncPoint(int(*func)(int *data))
{
    int i = 10;
    int *b = &i;
    printf("test func----\r\n");
    if (*func != NULL) {
        printf("start run func");
        *b = 100;
        int r = (*func)(b);
     
        
        printf ("\r\n cp ->python ->c %d",(int)i);
        printf ("\r\n python -> c %d\r\n",r);
    }
}

void testPointMessage(int(*func)(Message *message))
{
    Message m = {{1,2,44},3};
    
    if ((*func) != NULL) {
        printf("test point ----\r\n");
        (*func)(&m);
        printMessage(m);
    }
}




void testregiestMessage(void (*sendCallBack)(Message), Message(recvCallback)(void))
{
    unsigned char d[3]={40,48,55};
    Message m = {d,3};
    
    (*sendCallBack)(m);
    
    printMessage( (*recvCallback)() );
}


/***********************


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


n = m.load_address(0x80000000)

sendData(serPort, n)

sendData(serPort,m.read_flash([14, 00, 10, 20]))

n = m.cmd_leave_program_isp()

sendData(serPort,n)
 
********************/









