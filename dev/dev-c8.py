import time
import serial
import io


sync_bit = b'\xc8'

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    print('starting to read')
    
    while True:
        s = ser.read(100)
        chans = s[s.find(sync_bit):-1]
        # print(chans)
        # if len(chans) == 0:
        # 	chans = list(range(2000))
        # print(chans)
        if len(chans) > 15:
            chans = list(reversed(chans))
            
            print(
                    # 'chans',
                    # chans,
                    '',
                    f'{chans[-2]:5}',
                    f'{chans[-1]:5}',
                    'start'
    
                    f'{chans[-0]:5}',
                    f'{chans[-1]:5}',
                    f'{chans[-2]:5}',
                    f'{chans[-3]:5}',
                    f'{chans[-4]:5}',
                    f'{chans[-5]:5}',
                    f'{chans[-6]:5}',
                    f'{chans[-7]:5}',
                    f'{chans[-8]:5}',
                    f'{chans[-9]:5}',
                    f'{chans[-10]:5}',
                    f'{chans[-11]:5}',
                    f'{chans[-12]:5}',
                    f'{chans[-13]:5}',
                    f'{chans[-14]:5}',
                    f'{chans[-15]:5}',
                    'end',
                    f'{chans[16]:5}',
                    f'{chans[17]:5}',
                    f'{chans[18]:5}',
                    )
            
            # print(
            # 		'chans',
            # 		f'{hex(chans[-2]):5}',
            # 		f'{hex(chans[-1]):5}',
            # 		'start',
            # 		f'{hex(chans[0]):5}',
            # 		f'{hex(chans[1]):5}',
            # 		f'{hex(chans[2]):5}',
            #
            # 		f'{hex(chans[3]):5}',
            # 		f'{hex(chans[4]):5}',
            # 		f'{hex(chans[5]):5}',
            # 		f'{hex(chans[6]):5}',
            # 		f'{hex(chans[7]):5}',
            # 		f'{hex(chans[8]):5}',
            # 		)
            
