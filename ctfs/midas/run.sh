#!/bin/sh
qemu-system-x86_64 \
    -m 128M \
    -cpu kvm64,+smap,+smep \
    -kernel vmlinuz \
    -initrd initramfs.cpio \
    -hdb flag.txt \
    -snapshot \
    -nographic \
    -monitor /dev/null \
    -no-reboot \
    -gdb tcp::1234 \
    -append "console=ttyS0 kaslr pti=on quiet panic=1"
