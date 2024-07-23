#!/usr/bin/env python3

from pwn import *

exe = ELF("./rust_patched")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("addr", 1337)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


expected = [-42148619422891531582255418903, -42148619422891531582255418927, -42148619422891531582255418851, -42148619422891531582255418907, -42148619422891531582255418831, -42148619422891531582255418859, -42148619422891531582255418855, -42148619422891531582255419111, -42148619422891531582255419103, -42148619422891531582255418687, -42148619422891531582255418859, -42148619422891531582255419119, -42148619422891531582255418843, -42148619422891531582255418687, -42148619422891531582255419103, -42148619422891531582255418907, -42148619422891531582255419107, -42148619422891531582255418915, -42148619422891531582255419119, -42148619422891531582255418935,     -42148619422891531582255418823]


def main(msg):
    io = conn()
    io.sendlineafter(b"message:", msg.encode())
    io.sendlineafter(b"in hex", b"883085554737383682184979")
    io.recvuntil(b"Encrypted: ")
    out = eval(io.recvline())
    io.close()
    if out == expected[:len(out)]:
        return True
    return False
    
    

import string
if __name__ == "__main__":
    flag = "ictf{"
    while True:
        for c in string.printable:
            if main(flag+c):
                flag = flag+c
                print(flag)
                break
