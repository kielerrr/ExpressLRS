from com import communication
import time
import csv
import threading

def send_frame(called_at_time):
    global channel_flipper
    if channel_flipper == True:
        disarm_channels = [1400, 1500, 900, 1500, 1000, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500,
                           1500]
        com.update_data(disarm_channels)
    else:
        arm_channels = [1500, 1500, 900, 1500, 1000, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        com.update_data(arm_channels)

    in_function_time = time.perf_counter()
    # print(in_function_time, called_at_time)  # debug
    # print(in_function_time - called_at_time)  # debug
    # print()
    # time.sleep(1)


tik_time = time.perf_counter()
# crsf_tik_delay = 0
crsf_tik_delay = 0.004
crsf_trigger_time = tik_time
channel_flipper_delay = 1
channel_flip_trigger_time = tik_time
channel_flipper = True

com = communication(com_port='/dev/ttyUSB0')

thread = threading.Thread(target=com.transmit, daemon=True)
thread.start()
thread2 = threading.Thread(target=com.decode_telemetry, daemon=True)
thread2.start()

while True:
    if tik_time >= crsf_trigger_time:
        if tik_time >= channel_flip_trigger_time:
            channel_flipper = False if channel_flipper else True
            channel_flip_trigger_time = tik_time + channel_flipper_delay
        send_frame(tik_time)
        crsf_trigger_time = tik_time + crsf_tik_delay
    tik_time = time.perf_counter()

print('done sending')
# # csv settings
# csv_counter = 0
# dicts = []
# save_after = 100000  # seconds
# t1 = time.time()
# Increase and decrease the throttle in a loop and save the times in a csv file
# while True:
#     channels_pwm = [1500, 1500, 1050, 1500, 1800, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
#     com.update_data(channels_pwm)
#     data = {'time': time.time(), 'throttle': channels_pwm[2]}
#     dicts.append(data)
#     time.sleep(0.01)
#
#     channels_pwm = [1500, 1500, 1500, 1500, 1800, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
#     com.update_data(channels_pwm)
#     data = {'time': time.time(), 'throttle': channels_pwm[2]}
#     dicts.append(data)
#     time.sleep(0.01)
#
#     if (time.time()-t1) > save_after:
#         print("saving csv file")
#         com.update_data(disarm_channels)
#         keys = dicts[0].keys()
#
#         with open('command_data.csv', 'w', newline='') as output_file:
#             dict_writer = csv.DictWriter(output_file, keys)
#             dict_writer.writeheader()
#             dict_writer.writerows(dicts)
#
# print('done')
