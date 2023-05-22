#!/usr/bin/env python3
from operator import contains
from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial

from crsf_parser.payloads import PacketsTypes
from crsf_parser.handling import crsf_build_frame
import time


def print_frame(frame: Container, status: PacketValidationStatus) -> None:
    print(
        f"""
    {status}
    {frame}
    """
    )

interval = 0.05
next_call = time.time()
long_call = time.time()
# bit_cycle = [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\x09',b'\x0a',b'\x0b',b'\x0c',b'\x0d',b'\x0e',b'\x0f']
# bit_cycle = [b'\x00',b'\x00',b'\x00',b'\x01',b'\x02',b'\x04',b'\x08',b'\x10',b'\x20',b'\x40',b'\x80',b'\xff',b'\xff',b'\xff',b'\x00',b'\x00',b'\x00']
# bit_cycle = [b'\x00',b'\xfa',b'\xfb',b'\xfc',b'\xfd',b'\xfe',b'\xff']
bit_cycle = [b'\x00']
array_pointer = 0

crsf_parser = CRSFParser(print_frame)
with Serial("/dev/ttyUSB0", 115200, timeout=2) as ser:
    input = bytearray()
    while True:
        
        current_time = time.time()      
        
        if current_time >= long_call:
            array_pointer = array_pointer + 1 if (array_pointer != len(bit_cycle) -1) else 0
            bit = bit_cycle[array_pointer]
            long_call = time.time() + 1/2
        if current_time >= next_call:
            ser.write(bit)            
            next_call += interval
        
            
        time.sleep(0.001)
        
        # if n == 0:
        #     n = 10
        #     frame = crsf_build_frame(
        #         PacketsTypes.BATTERY_SENSOR,
        #         {"voltage": v, "current": 1, "capacity": 100, "remaining": 100},
        #     )
        #     v += 1
        #     ser.write(frame)
        #     ser.write(b'\xee\x04\x28\x00\xea\x54')
        #     ser.write(b'\xbe\xef\xBa\xbe\xca\xfe\xf0\x0d')
        # n = n - 1
        # values = ser.read(100)
        # print(values)
        # input.extend(values)
        # crsf_parser.parse_stream(input)
