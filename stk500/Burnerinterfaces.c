
#include"mega1280Protect.h"
#include<stdlib.h>

typedef enum{
    STATUS_OK,
    STATUS_FAILED,
    STATUS_TIMEOUT
} Status;

typedef  void (*sendFunc_p) (Message message);
typedef Message (*recvFunc_p) ();

static sendFunc_p _sendfun_p;
static recvFunc_p _recvfunc_p;


void regestFunc(sendFunc_p sendfunc,recvFunc_p recvfunc)
{
    _sendfun_p = sendfunc;
    _recvfunc_p = recvfunc;
}


Message processData(Message message)
{
    Message result = {};
    int size = 0;
    if (message.size >= 6) {
        if (message.data[0] == 0x1b && message.data[4] == 0x0e ) {
            size = ((message.data[2]>>8)&0xff) +((message.data[3])&0xff);
            unsigned char *c_data = malloc(size * sizeof(unsigned char));
            
            for (int i = 0; i < size; i++) {
                c_data[i] = message.data[i+5];
            }
            result.data = c_data;
            result.size = size;
        }else
        {
            printf("data error -- no flags\r\n");
        }
    }
    else{
        printf("data error -- no data\r\n");
    }
    
    free(message.data);
    return result;
}


Message sendAndRecv(Message message,sendFunc_p sendfunc,recvFunc_p recvfunc)
{
    Message result;

    if (*sendfunc != NULL)
    {
        (*sendfunc)(message);
    }else{
        printf("cannot send data ,please check interface \r\n");
    }
    if (*recvfunc != NULL)
    {
       result = (*recvfunc)();
    }
    else
    {
        printf("cannot recieve data ,please check interface \r\n");
    }
    result = processData(result);
    return result;
}


Status startBurner()
{
    Message m = sign_on();
    Message result = sendAndRecv(m,_sendfun_p ,_recvfunc_p);
    
    if (result.size) {
        
        return STATUS_OK;
    }
    
    return STATUS_FAILED;
}

Status signOn()
{
    Message m = sign_on();
    
    Message result = sendAndRecv(m, _sendfun_p ,_recvfunc_p);
   
    if (result.size) {
        
        if (messageContentMessage( messageFromString('AVRISP_2') )) {
            
            return STATUS_OK;
        }
    }
    return STATUS_FAILED;
}

Status enterIsporgram()
{
    Message r = cmd_enter_progmode_isp(0xc8, 0x64, 0x19, 0x20, 0x00, 0x53, 0x03, 0xac, 0x53, 0x00, 0x00);
    
    Message result = sendAndRecv(r, _sendfun_p ,_recvfunc_p);
    
    if (result.size) {
        
        if (result.data[1] == 0) {
            
            return STATUS_OK;
        }
    }
    return STATUS_FAILED;
}



Status get_signature_byte(unsigned char *d)
{
    Message m = {d,4};
    
    m = spi_multi(0x04,m,0);
    
    Message result = sendAndRecv(m,_sendfun_p ,_recvfunc_p);
    
    if (result.size) {
        
        if (result.data[1] == 0) {
            
            return STATUS_OK;
        }
    }
    return STATUS_FAILED;
    
}

Status signature_byte()
{
    Status t;
    unsigned char* d = {0x30,0,0,0};
    for (int i = 0; i < 3 ; i++) {
        d[2] = i;
      Status x =  get_signature_byte(d);
        
        if (x!=STATUS_OK) {
            t = STATUS_FAILED;
        }
    }
    
    return t;
}

Status load_program_address(unsigned int add)
{
    Message m = load_address(add);
    Message result = sendAndRecv(m,_sendfun_p,_recvfunc_p);
    
    if (result.size) {
        
        if (result.data[1] == 0) {
            
            return STATUS_OK;
        }
    }
    return STATUS_FAILED;
}

Status write_program_flash(unsigned char*d ,unsigned int size)
{
    Message m = {d, size};
    
    int bh = (size>>8)&0x00ff;
    int bl = (size)&0x00ff;
    
    m = cmd_program_flash_isp(bh,bl,0xc1,0x0a,0x40,0x4c,0x20,0,0,m);
    
    Message result = sendAndRecv(m,_sendfun_p,_recvfunc_p);
    
    if (result.size) {
        
        if (result.data[1] == 0) {
            
            return STATUS_OK;
        }
    }
    return STATUS_FAILED;
}





///
void Burner(void)
{
    while ( !sign_on() );
    
    enterIsporgram();
    
    signature_byte();
    
    load_program_address(0x8000);
    
    write_program_flash();
    
}

















