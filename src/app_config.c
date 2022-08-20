#include "sl_sleeptimer.h"
#include "app_config.h"
sl_sleeptimer_timer_handle_t send_config_timer;
static bool send_config_flag = true;


/***************************************************************************//**
 * Sends JSON configuration over iostream.
 ******************************************************************************/
static void send_json_config(void);

// -----------------------------------------------------------------------------
// Public function definitions

static void send_config_callback(sl_sleeptimer_timer_handle_t *handle, void *data)
{
  (void)handle;
  (void)data;
  send_config_flag = true;
}

/***************************************************************************//**
 * Setup periodic timer for sending configuration messages.
 ******************************************************************************/
void app_config_json(void)
{
  /* Set up periodic JSON configuration timer. */
  sl_sleeptimer_start_periodic_timer_ms(&send_config_timer, JSON_TEMPLATE_INTERVAL_MS, send_config_callback, NULL, 0, 0);

  // Send initial JSON config message
  send_json_config();
}


/***************************************************************************//**
 * JSON configuration message ticking function.
 ******************************************************************************/
void app_config_process_action_config(void)
{
  if (send_config_flag == true) {
    send_json_config();
    send_config_flag = false;
  }
}


static void send_json_config()
{
  printf("{\"version\":%d, \"sensors\": [{\"channel\":%d,\"sample_rate\":%d,"
      "\"column_location\":{"
      "\"Microphone\":0},"
      "\"samples_per_packet\":%d},"
      "{\"sample_rate\":%d,\"channel\":%d,"
      "\"samples_per_packet\":%d,"
    "\"column_location\":{"
    "\"AccelerometerX\":0,"
    "\"AccelerometerY\":1,"
    "\"AccelerometerZ\":2}}]}\n",
     3, SSI_CHANNEL_AUDIO, SR2FS(VOICE_SAMPLE_RATE_DEFAULT),  MIC_SAMPLE_BUFFER_SIZE, ACCEL_GYRO_ODR, SSI_CHANNEL_IMU, APP_IMU_SAMPLES_PER_PACKET);\
}
