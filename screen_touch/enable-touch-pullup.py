#!/usr/bin/env python3
import mmap, struct

with open('/dev/mem', 'r+b') as f:
    m = mmap.mmap(f.fileno(), 4096, offset=0x0300B000)
    
    # 1. Enable pull-up on PC8 (TOUCH_IRQ): Bank C PULL0 is at offset 0x64, pin 8 is bits 16..17
    c_pull0 = struct.unpack('<I', m[0x64:0x68])[0]
    c_pull0 &= ~(3 << 16)
    c_pull0 |= (1 << 16)
    m[0x64:0x68] = struct.pack('<I', c_pull0)
    
    # 2. Enable pull-up on PH9 (TOUCH_CS): Bank H PULL0 is at offset 0x118, pin 9 is bits 18..19
    h_pull0 = struct.unpack('<I', m[0x118:0x11C])[0]
    h_pull0 &= ~(3 << 18)
    h_pull0 |= (1 << 18)
    m[0x118:0x11C] = struct.pack('<I', h_pull0)

print("Touch hardware pull-ups enabled: PC8=1, PH9=1")
