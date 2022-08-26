/***************************************************************************//**
 * @file
 * @brief Top level application functions
 *******************************************************************************
 * # License
 * <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided \'as-is\', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 *******************************************************************************
 * # Experimental Quality
 * This code has not been formally tested and is provided as-is. It is not
 * suitable for production environments. In addition, this code will not be
 * maintained and there may be no bug maintenance planned for these resources.
 * Silicon Labs may update projects from time to time.
 ******************************************************************************/
#include <stdbool.h>

#include "app_iostream_usart.h"
#include "app_voice.h"
#include "app_led.h"
#include "app_config.h"
#include "sl_sleeptimer.h"
#include "em_gpio.h"

volatile bool config_received = false;
sl_sleeptimer_timer_handle_t time_stamp_timer;
uint32_t time_stamp = 0;

static void on_timeout (sl_sleeptimer_timer_handle_t *handle, void *data)
{
  time_stamp++;
}
void app_init (void)
{

  sl_sleeptimer_start_periodic_timer_ms (&time_stamp_timer,
  TIMER_RESOLUTION_MS,
                                         on_timeout, NULL, 0,
                                         SL_SLEEPTIMER_NO_HIGH_PRECISION_HF_CLOCKS_REQUIRED_FLAG);
  app_iostream_usart_init ();

  app_config_json ();

  app_led_init ();
}

void app_process_action (void)
{
  // Send JSON configuration and wait to receive "connect" command
  if (!config_received)
    {
      app_config_process_action_config ();
      app_iostream_usart_process_action ();
    }
  else
    { // once connected, no longer necessary to listen for commands
      app_iostream_usart_process_action ();
      app_sensor_imu_process_action ();
      app_voice_process_action ();
    }

  app_led_process_action ();
}
