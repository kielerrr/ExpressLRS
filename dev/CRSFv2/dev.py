#!/usr/bin/env python3
from operator import contains
from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial

from crsf_parser.payloads import PacketsTypes
from crsf_parser.handling import crsf_build_frame
import time


interval = 0.004
# interval = 0.00
next_call = time.time()
long_call = time.time()
bit_cycle = [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\x09',b'\x0a',b'\x0b',b'\x0c',b'\x0d',b'\x0e',b'\x0f']
# bit_cycle = [b'\x00',b'\x00',b'\x00',b'\x01',b'\x02',b'\x04',b'\x08',b'\x10',b'\x20',b'\x40',b'\x80',b'\xff',b'\xff',b'\xff',b'\x00',b'\x00',b'\x00']
# bit_cycle = [b'\x00',b'\xfa',b'\xfb',b'\xfc',b'\xfd',b'\xfe',b'\xff']
array_pointer = 0

with Serial("/dev/ttyUSB0", 115200, timeout=2) as ser:
    while True:

        current_time = time.time()

        # if current_time >= long_call:
        #     array_pointer = array_pointer + 1 if (array_pointer != len(bit_cycle) - 1) else 0
        #     bit = bit_cycle[array_pointer]
        #     long_call = time.time() + 1 / 2
        # if current_time >= long_call:
        #     interval = interval + 0.0001
        #     long_call = time.time() + 2
        #     print(interval)
        if current_time >= next_call:
            # ser.write(b'\xee\x17\x16\xe1\xe3\xde\x09\xc7\xd7\x8a\x56\x80\x0f\x7c\xe0\x03\x1f\xf8\xc0\x07\x3e\xf0\x81\x0f\x7c\x36')
            ser.write(b'\xee\x18\x16\xe7\x0b\x1f\xf8\xc0\x37\xf1\x56\xb4\xa2\x15\xe0\x03\x1f\xf8\xc0\x07\x3e\xf0\x81\x0f\x7c\x0c\x00')
            ser.write(b'\xEA\x0D\x3A\xEE\xEE\x10\x00\x01\x04\x64\xFF\xFF\xFD\x30\x42')
            #print('done')
            # ser.write(b'\x000000000')
            # ser.write(b'\x10101010101')
            # ser.write(b'\x000000000')
            # print(time.time())
            next_call += interval

        # time.sleep(0.004)
