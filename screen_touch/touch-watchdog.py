#!/usr/bin/env python3
import time
import glob
import os
import sys
import select

hwmon_files = glob.glob('/sys/bus/spi/devices/spi1.0/hwmon/*/in0_input')
if not hwmon_files:
    sys.exit(1)
hwmon_path = hwmon_files[0]

def rearm():
    try:
        with open(hwmon_path, 'r') as f:
            f.read()
    except Exception:
        pass

# Always rearm on start
rearm()

ev_fd = None
try:
    ev_fd = os.open('/dev/input/event0', os.O_RDONLY | os.O_NONBLOCK)
except Exception:
    pass

while True:
    try:
        if ev_fd is not None:
            r, _, _ = select.select([ev_fd], [], [], 1.5)
            if r:
                try:
                    os.read(ev_fd, 1024)
                except Exception:
                    pass
            else:
                # 1.5s idle timeout - rearm XPT2046 PENIRQ
                rearm()
        else:
            time.sleep(1.5)
            rearm()
    except Exception:
        time.sleep(1.5)
        rearm()
