# SensiML xG24 Microphone and IMU Data Capture Example

## Summary

This project uses the EFR32xG24 Dev Kit Board with the onboard IMU and I2S microphone sensosr to take audio and motion measurements and send data via serial UART. A basic python script is also provided to capture the data and store as a wav file for the audio and a CSV file for the IMU data. The example project uses the I/O Stream service along with Microphone and IMU component drivers running in a bare-metal configuration. Sensor data from the I2S Microphone and the SPI IMU is transferred over virtual COM port (VCOM) at 921600 baud. The sensor data output data rate is configured at 16 kHz while the IMU is set to sample at 102.3 Hz.

Software Components used: I2S Microphone, Simple LED, IO Stream: USART, Sleeptimer, IMU

## Gecko SDK version

v4.02

## Hardware Required

- One EFR32xG24 Dev Kit Board (Link currently unavailable)

- One micro USB cable

## Data Capture Lab Projects

The data for the included project can be found ere

[Smart Lock IMU Data](https://sensiml-data-depot.s3.us-west-2.amazonaws.com/workswith-2022/Smart_Lock_IMU.zip)
[Smart Lock Audio Data](https://sensiml-data-depot.s3.us-west-2.amazonaws.com/workswith-2022/Smart_Lock_Audio.zip)


## Setup

Import the included .sls file to Studio then build and flash the project to the SLTB004A development kit.
In Simplicity Studio select "File->Import" and navigate to the directory with the .sls project file.
The project is built with relative paths to the STUDIO_SDK_LOC variable which was defined as

C:\SiliconLabs\SimplicityStudio\v5\developer\sdks\gecko_sdk_suite\v4.0

In Simplicity Studio, under the Debug Adapters window, right-click on the EFR32xG24 Dev Kit Board device and select "Launch console..." from the drop-down menu. In the Adapter Console window, select the "Admin" tab and type "serial vcom config speed 921600" into the terminal input. This will modify the VCOM baudrate to match the application settings. If making any changes to the USART baudrate, the baudrate change must also be modified in the VCOM debug adapter settings.

## How the Project Works

The application uses the process-action bare-metal project configuration model. First, the IO Stream/USART are configured for 8 bit, no parity, 1 stop bit, and 921600 baudrate. A periodic sleep timer is also configured with 1 second interrupt. Within the application's process actions, the serial input is monitored for a connection command expected from SensiML's Data Capture Lab (DCL). A JSON configuration packet is sent via USART/VCOM to the PC once per second (via sleep timer) until the connection command is received, at which point the application halts monitoring the serial input and sending configuration information. The I2S Microphone and IMU are initialized and data is sent to PC at the specified data rate (default setting is 16 kHz for audio and 102.3 for IMU). The onboard LEDs are also used to indicate that the application is running (blinking green LED at 2 Hz) and when the application is waiting for the connection command (solid red LED). Once connected, the red LED will turn off. Upon disconnecting from SensiML, the red LED will be turned on again and the device will resume sending configuration packets. The device can be reconnected without a reset.

The audio output data rate is hard-coded in the application in "app_voice.c" defined as VOICE_SAMPLE_RATE_DEFAULT (line 32) using the enumeration "sample_rate_t" found in "app_voice.h" starting at line 23. Two data rates are available, 8 KHz and 16 kHz (default setting). The IMU data rate is set by modifying the ACCEL_GYRO_DEFAULT_ODR constant in the header file app_sensor_imu.h

## .sls Projects Used

SensiML_Microphone_data_capture.sls

## How to Port to Another Part

Open the "Project Properties" and navigate to the "C/C++ Build -> Board/Part/SDK" item. Select the new board or part to target and "Apply" the changes. Note: there may be dependencies that need to be resolved when changing the target architecture.

## Known issue

Currently due to the architecture of the drivers, higher sampling rates for the IMU are not possible. Current measurements indicate a practical limit of around 2000Hz.

## Record Sensor Data

You can use the python script /python/record.py to record sensor data from both the IMU and Audio which will be synced when written to a csv and wav file respectively.

> cd python
> pip install -r requirements.txt
> python record.py
