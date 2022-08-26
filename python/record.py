import serial
import serial.tools.list_ports
import soundfile as sf
import time
import numpy as np
import json
import os
from collections import namedtuple

6
Header = namedtuple("Header", ["data_size", "rsvd", "channel", "sequence_number"])


def get_config(port: str, baud_rate: int):
    with serial.Serial(port, baud_rate, timeout=1) as ser:
        ser.write(b"disconnect")
        time.sleep(1)
        ser.readline()
        value = ser.readline().decode("ascii")

        return json.loads(value)


def get_port_info():
    ports = serial.tools.list_ports.comports()

    port_list = []
    for index, (port, desc, hwid) in enumerate(sorted(ports)):
        port_list.append({"id": index, "name": desc, "device_id": port})

    return port_list


class RecordSensor(object):
    def __init__(self, file_prefix: str, port: str, baud_rate: int):
        self.file_prefix = file_prefix
        self.channel_data = []
        self.config = get_config(port, baud_rate)
        self.data = {}

    def write_buffer(self, channel: int):

        num_cols = self.data[channel]["num_columns"]
        data = self.data[channel]["data_buffer"]
        print(
            "writing channel",
            channel,
            "data size",
            len(data),
            "to",
            self.data[channel]["filename"] + ".csv",
        )
        with open(self.data[channel]["filename"] + ".csv", "w") as out:
            out.write(",".join(self.data[channel]["columns"].keys()) + "\n")

            for index in range(len(data) // num_cols):
                out.write(
                    ",".join([str(data[index * num_cols + i]) for i in range(num_cols)])
                    + "\n"
                )

        if self.data[channel]["columns"].get("Microphone") == 0:
            sf.write(
                self.data[channel]["filename"] + ".wav",
                np.array(data, dtype=np.int16),
                self.data[channel]["sample_rate"],
            )

        self.data[channel]["data_buffer"] = []

        return len(data) // num_cols

    def write_buffers(self):
        data_size = {}
        for channel in self.data:
            data_size[channel] = self.write_buffer(channel)

        return data_size

    @staticmethod
    def get_packet_header(ser):

        # Get size
        byte_array = ser.read() + ser.read()

        data_size = int.from_bytes(byte_array, "little")

        # get rsvd
        byte_array = ser.read()
        rsvd = int.from_bytes(byte_array, "little")

        byte_array = ser.read()
        channel = int.from_bytes(byte_array, "little")

        # read sequence number
        byte_array = ser.read() + ser.read() + ser.read() + ser.read()

        sequence_number = int.from_bytes(byte_array, "little")

        return Header(data_size, rsvd, channel, sequence_number)

    def get_packet_data(self, ser: serial, header: Header):

        for i in range((header.data_size - 6) // 2):
            byte_array = ser.read() + ser.read()
            data_point = int.from_bytes(byte_array, "little", signed="True")
            self.data[header.channel]["data_buffer"].append(data_point)

    def find_sync(self, ser: serial):
        found_sync = False
        while not found_sync:
            char_in = ser.read()
            if char_in == b"\xff":
                found_sync = True

    def get_packets(self, ser: serial):
        self.find_sync(ser)
        header = self.get_packet_header(ser)
        self.get_packet_data(ser, header)
        data_byte = ser.read()
        checksum = int.from_bytes(data_byte, "little")

    def connect(self, record_time: int, port: str, baud_rate: int):
        with serial.Serial(port, baud_rate, timeout=1) as ser:
            ser.reset_input_buffer()
            print("Connecting")
            ser.write(b"connect")
            start = time.time()

            print("Recording for", record_time, "seconds")
            print(0)
            curr_time = 0
            while record_time > time.time() - start:
                if int(time.time() - start) != curr_time:
                    curr_time = int(time.time() - start)
                    if curr_time % 5 == 0:
                        print(curr_time)

                self.get_packets(ser)
            print(curr_time)
            recorded_time = time.time() - start

            ser.write(b"disconnect")

            return recorded_time

    def init(self, filename_map=None, initial_index=0):
        for sensor_config in self.config["sensors"]:

            if filename_map and filename_map.get(sensor_config["channel"]):
                channel_name = filename_map.get(sensor_config["channel"])
            else:
                channel_name = "channel{index}".format(index=sensor_config["channel"])

            filename = "{prefix}_{channel_name}".format(
                prefix=self.file_prefix, channel_name=channel_name
            )

            filename += get_recording_index(filename, initial_index=initial_index)

            self.data[sensor_config["channel"]] = {
                "filename": filename,
                "data_buffer": [],
                "num_columns": len(sensor_config["column_location"]),
                "sample_rate": sensor_config["sample_rate"],
                "columns": sensor_config["column_location"],
            }


def get_recording_index(filename, initial_index=0):
    suffix = f"_{initial_index}"
    counter = initial_index + 1
    while os.path.exists(filename + suffix + ".csv"):
        suffix = f"_{counter}"
        counter += 1

    return suffix


def summarize_recording(record_time, data_sizes, recorder):
    for channel in data_sizes.keys():
        print(
            "channel",
            channel,
            "record_time",
            record_time,
            "recorded",
            int(recorded_time),
            "expected",
            record_time * recorder.data[channel]["sample_rate"],
            "actual",
            data_sizes[channel],
            "calculated",
            int(data_sizes[channel] / recorded_time),
        )


if __name__ == "__main__":

    COM_PORT = ""  # "COM4"
    RECORD_TIME = 10  # Seconds
    BAUD_RATE = 921600
    FILE_PREFIX = "record_session"
    FILENAME_MAP = {1: "audio", 2: "imu"}
    INITIAL_INDEX = 21

    if not COM_PORT:
        port_list = get_port_info()
        COM_PORT = port_list[0]["device_id"]

    config = get_config(COM_PORT, BAUD_RATE)

    print("Retrieved Config")
    print(json.dumps(config, indent=4, sort_keys=True))

    filenames = []

    recorder = RecordSensor(FILE_PREFIX, COM_PORT, BAUD_RATE)
    recorder.init(filename_map=FILENAME_MAP, initial_index=INITIAL_INDEX)

    recorded_time = recorder.connect(RECORD_TIME, COM_PORT, BAUD_RATE)

    data_sizes = recorder.write_buffers()

    summarize_recording(recorded_time, data_sizes, recorder)
