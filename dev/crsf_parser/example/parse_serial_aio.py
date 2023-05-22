#!/usr/bin/env python3
from operator import contains
from typing import Container
from crsf_parser import CRSFParser, PacketValidationStatus
from serial import Serial

from crsf_parser.payloads import PacketsTypes
from crsf_parser.handling import crsf_build_frame

from crsf_parser import crsf_frame



def print_frame(frame: Container, status: PacketValidationStatus) -> None:
    print(
        f"""
    {status}
    {frame}
    """
    )


crsf_parser = CRSFParser(print_frame)
n = 10
v = 1

try:
    serial_tx = Serial("/dev/ttyUSB0", 420000, timeout=2)
    serial_tx.close()
    serial_tx.open()
except:
    pass

try:
    serial_rx =  Serial("/dev/ttyUSB2", 420000, timeout=2)
    serial_rx.close()
    serial_rx.open()
except:
    pass


input = bytearray()
while True:
    frame = crsf_build_frame(
        PacketsTypes.RC_CHANNELS_PACKED,
        # {"channels": [200, 200, 200, 200, 200, 200, 200, 244, 200, 200, 200, 200, 200, 200, 200, 200]},
        {"channels": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]},
    )    
    # data = crsf_frame.parse(frame)
    # print(crsf_frame.header.data_offset)
    # print(data, type(data))
    # print(frame, len(frame), type(frame))

    print(frame)
    serial_tx.write(frame)
    # values = serial_rx.read(100)
    # input.extend(values)
    # crsf_parser.parse_stream(input)    
        
serial_rx.close()
serial_tx.close()
