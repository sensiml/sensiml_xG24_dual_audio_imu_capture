#ifndef APP_CONFIG_H
#define APP_CONFIG_H

#include <stdbool.h>
#include <stdint.h>

// IMU ODR settings. Note: Gyroscope and Accel are linked.
typedef enum
{
    // Sample Rate 0:4.4Hz, 1:17.6Hz, 2:35.2Hz, 3:48.9Hz, 4:70.3Hz, 5:102.3HZ...
    ACCEL_GYRO_ODR_4p4HZ   = 0,
    ACCEL_GYRO_ODR_17p6HZ  = 1,
    ACCEL_GYRO_ODR_35p2HZ  = 2,
    ACCEL_GYRO_ODR_48p9HZ  = 3,
    ACCEL_GYRO_ODR_70p3HZ  = 4,
    ACCEL_GYRO_ODR_102p3HZ = 5,
    ACCEL_GYRO_ODR_140p6HZ = 6,
    ACCEL_GYRO_ODR_187p5HZ = 7,
    ACCEL_GYRO_ODR_281p3HZ = 8,
    ACCEL_GYRO_ODR_562p5HZ = 9,
} accel_gyro_odr_t;


typedef enum {
  sr_8k = 8,
  sr_16k = 16,
} sample_rate_t;

#define SSI_CHANNEL_AUDIO          (1)
#define SSI_CHANNEL_IMU            (2)

#define VOICE_SAMPLE_RATE_DEFAULT sr_16k
#define VOICE_CHANNELS_DEFAULT    1
#define VOICE_FILTER_DEFAULT      true
#define VOICE_ENCODE_DEFAULT      false
#define MIC_SAMPLE_BUFFER_SIZE  112
#define SR2FS(sr)               ((sr) * 1000)

// Default sample rates.
//#define ACCEL_GYRO_DEFAULT_ODR ACCEL_GYRO_ODR_102p3HZ
#define ACCEL_GYRO_DEFAULT_ODR ACCEL_GYRO_ODR_102p3HZ
#define ACCEL_GYRO_ODR 102
#define APP_IMU_SAMPLES_PER_PACKET     10



/** Time (in ms) between periodic JSON template messages. */
#define JSON_TEMPLATE_INTERVAL_MS      1000

#define TIMER_RESOLUTION_MS            10

void app_config_json(void);

#endif //__APP_CONFIG_H
