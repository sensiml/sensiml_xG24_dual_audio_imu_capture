# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import serial
import soundfile as sf
import numpy as np
import time

data_size = 0
channel = -1
senquence_number = -1
data_file_1 = 'channel1.csv'
data_file_2 = 'channel2.csv'
channel1_data = []
channel2_data = []

def init_files():
    file1 = open(data_file_1, "w")
    file1.write("channel_0\n")
    file1.close()
    file2 = open(data_file_2, "w")
    file2.write("AccelerometerX,AccelerometerY,AccelerometerZ\n")
    file2.close()

def append_channel_1(data):

    with open(data_file_1, "a") as file1:
        for item in data:
            file1.write(str(item)+"\n")

    sf.write('channel1.wav', np.array(data, dtype=np.int16), 16000)

    return len(data)

def append_channel_2(data):
    with open(data_file_2, "a") as file2:
        for i in range(len(data) // 3):
         file2.write(str(data[i*3])+","+str(data[(i*3)+1])+","+str(data[(i*3)+2])+"\n")

    return len(data)//3


def get_header(s):
    global data_size
    global channel
    # Get size
    byte_array = s.read() + s.read()

    data_size = int.from_bytes(byte_array, 'little')
    # get rsvd
    byte_array = s.read()
    rsvd = int.from_bytes(byte_array, 'little')

    byte_array = s.read()
    channel = int.from_bytes(byte_array, 'little')

    # read sequence number
    byte_array = s.read() + s.read() + s.read() + s.read()

    sequence_number = int.from_bytes(byte_array, 'little')

def get_data(s):

    global channel1_data;
    global channel2_data;
    for i in range((data_size - 6) // 2):
        byte_array = s.read() + s.read()
        data_point = int.from_bytes(byte_array, 'little',signed="True")
        if channel == 1:
            channel1_data.append(data_point)
        if channel == 2:
            channel2_data.append(data_point)

def find_sync(s):
    found_sync = False
    while not found_sync:
        char_in = s.read()
        if char_in == b'\xff':
            found_sync = True



def get_packets(s):
    find_sync(s)

    get_header(s)

    get_data(s)
    data_byte = s.read()
    checksum = int.from_bytes(data_byte, 'little')

def startup(record_time, port, baud_rate):
    with serial.Serial(port, baud_rate, timeout=1) as s:
        s.reset_input_buffer()
        #print('sending connect')
        s.write(b"connect")
        start = time.time()
        #print("record time is ", record_time, 'seconds')
        while record_time > time.time() - start:
            get_packets(s)
        record_time= time.time()- start


        s.write(b"disconnect")

        return record_time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    COM_PORT = "COM9"
    BAUD_RATE = 921600
    RECORD_TIME= 60
    AUDIO_SAMPLE_RATE=16000
    IMU_SAMPLE_RATE= 281.3  #really 111.11
    init_files()
    #for record_time in  range(1,20,5):
    record_time = RECORD_TIME;
    channel1_data = []
    channel2_data = []
    recorded_time =   startup(record_time, COM_PORT, BAUD_RATE)
    data_size  = append_channel_1(channel1_data)
    print("record_time", record_time, "recorded", int(recorded_time), "expected", record_time * AUDIO_SAMPLE_RATE,'actual', data_size,'calculated',int(data_size/recorded_time))
    data_size =  append_channel_2(channel2_data)
    print("record_time", record_time,"recorded", int(recorded_time), "expected", record_time * IMU_SAMPLE_RATE, 'actual', data_size,'calculated',data_size/recorded_time)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
