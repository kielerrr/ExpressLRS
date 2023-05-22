import serial
import time
from utils import us_to_ticks, ticks_to_us, pack_channels, crc_transmit


class communication():

    def __init__(self, com_port):
        self.ser = serial.Serial(com_port, baudrate=115200, timeout=1)
        # self.ser = serial.Serial(com_port, baudrate=416666, timeout=0)
        self.payload = []
        self.crc = []
        self.message = []
        self.t1 = 0
        self.received_bytes = None

    def transmit(self):
        self.t1 = time.time()
        read = False
        while True:
            t2 = time.time()
            dt = (t2-self.t1)*1000.0  # delta t in milliseconds

            # handle read buffer after telemetry is received (i.e. after 3ms for 150Hz(:6.67ms))
            if 3 < dt and not read:
                waiting = self.ser.in_waiting
                data = self.ser.read(waiting)
                if data != b'':
                    self.received_bytes = data
                read = True

            # write new frame
            if dt >= 6.666667:
                self.t1 = time.time()
                read = False
                self.ser.write(bytearray(self.message))
                # print('writinggg')
                self.ser.write(b'\xee\x17\x16\xe1\xe3\xde\x09\xc7\xd7\x8a\x56\x80\x0f\x7c\xe0\x03\x1f\xf8\xc0\x07\x3e\xf0\x81\x0f\x7c\x36')
                self.ser.write(b'\xEA\x0D\x3A\xEE\xEE\x10\x00\x01\x04\x64\xFF\xFF\xFD\x30\x42')

    def decode_telemetry(self):
        while True:
            if self.received_bytes is not None:
                rcv_list = list(self.received_bytes)
                # each received list must hold transmitted frame(26 bytes) and telemetry, so should be larger
                possible_telemetry_indices = [i for i, x in enumerate(rcv_list) if x == 234] # 234 = b'\ea'
                for i in possible_telemetry_indices:
                    telemetry_list = rcv_list[i:]
                    # check if address byte is correct
                    tel_type = telemetry_list[2]
                    if tel_type == 8:  # 0x08: battery sensor
                        # int16_t voltage (100*mV)
                        # int16_t current (100*mA)
                        # int24_t capacity used (mAh)
                        # int8_t battery remaining (percent)
                        voltage = int.from_bytes(bytearray(telemetry_list[3:5]), "big")
                        print(f'voltage: {voltage}')
            time.sleep(0.0001)

    def update_data(self, channels_pwm):
        # convert pwm values to rc values
        channels_rc = us_to_ticks(channels_pwm)
        print(channels_rc)

        # pack 16 channels to 22 bytes
        packed_channel = pack_channels(channels_rc)

        # calculate crc
        crc = crc_transmit([0x16], packed_channel)
        crc = [int(crc, 16)]

        self.payload = packed_channel
        self.crc = crc
        self.message = [0xee, 0x18, 0x16] + self.payload + self.crc
