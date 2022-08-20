/***************************************************************************//**
 * @file
 * @brief Inertial Measurement Unit sensor header
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


#ifndef APP_SENSOR_IMU_H
#define APP_SENSOR_IMU_H

#include "app_config.h"
#include "sl_status.h"



/**************************************************************************//**
 * Configure periodic timer and send configuration information
 *****************************************************************************/
void app_config_imu(void);

/**************************************************************************//**
 * JSON configuration ticking function
 *****************************************************************************/
void app_config_process_action_imu(void);

/**************************************************************************//**
 * IMU sensor ticking function
 *****************************************************************************/
void app_sensor_imu_process_action(void);

/**************************************************************************//**
 * Initialize IMU sensor.
 *****************************************************************************/
void app_sensor_imu_init(void);

/**************************************************************************//**
 * Deinitialize IMU sensor.
 *****************************************************************************/
void app_sensor_imu_deinit(void);

/**************************************************************************//**
 * Enable/disable IMU sensor.
 * @param[in] Enable (true) or disable (false).
 *****************************************************************************/
void app_sensor_imu_enable(bool enable);

/**************************************************************************//**
 * Getter for orientation and acceleration sensor measurement data.
 * @param[out] ovec Three dimensional orientation vector (in 0.01 degree).
 * @param[out] avec Three dimensional acceleration vector.
 * @return Status of the operation.
 *****************************************************************************/
sl_status_t app_sensor_imu_get(int16_t avec[3]);

#endif // SL_SENSOR_IMU_H
