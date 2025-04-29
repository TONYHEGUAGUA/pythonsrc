
#it can let drone fly in 0.5m/s to the left permantly

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil 

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


vehicle = connect('127.0.0.1:14550', wait_ready=True)



left_speed = 0.5  # 设置向左飞行速度为0.5m/s
flight_time = 2    # 飞行时间4秒（0.5m/s × 4s = 2米）

# 获取起始位置
start_position = vehicle.location.global_relative_frame



# 发送向左速度指令
msg = vehicle.message_factory.set_position_target_local_ned_encode(
    0,       # 时间戳
    0, 0,    # 目标系统ID和目标组件ID
    mavutil.mavlink.MAV_FRAME_BODY_NED,  # 坐标系
    0b0000111111000111, # 控制速度的位掩码
    0, 0, 0, # 位置参数（忽略）
    0, -left_speed, 0, # 速度参数（X,Y,Z）- Y为负表示向左
    0, 0, 0, # 加速度参数（忽略）
    0, 0)    # 偏航参数（忽略）


arm_and_takeoff(10)
while(1):
	vehicle.send_mavlink(msg)
	#vehicle.flush()
	print("in flying")

