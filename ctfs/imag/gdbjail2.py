from pwn import *

context.bits = 64
context.arch = 'amd64'

a = shellcraft.amd64.linux.execve("/bin/sh")
out = asm(str(a))
while len(out) % 8 != 0:
    out += b"\x00"
print(out)

to_send = []
for i in range(0, len(out), 4):
    n = int.from_bytes(out[i:i+4], 'little')
    print(f"set *{0x7ffff7ea37d0+i}={n}")
