from dronekit import connect
import time
vehicle = connect('127.0.0.1:14550' , wait_ready=True,rate=30)

# 连接飞控

# 实时打印位置和速度
while True:
    # 姿态角（弧度转角度）
        pitch_deg = vehicle.attitude.pitch * 57.2958
        roll_deg = vehicle.attitude.roll * 57.2958
        yaw_deg = vehicle.attitude.yaw * 57.2958

        # 位置信息
        loc_rel = vehicle.location.global_relative_frame
        loc_abs = vehicle.location.global_frame

        # 打印所有参数
        print("\n======= 飞行参数 =======")
        print(f"姿态角: Pitch={pitch_deg:.2f}°, Roll={roll_deg:.2f}°, Yaw={yaw_deg:.2f}°")
        print(f"相对位置: 经度={loc_rel.lon:.6f}, 纬度={loc_rel.lat:.6f}, 高度={loc_rel.alt:.2f}m")
        print(f"绝对高度: {loc_abs.alt:.2f}m AMSL")
        print(f"速度: 北向={vehicle.velocity[0]:.2f}m/s, 东向={vehicle.velocity[1]:.2f}m/s, 地速={vehicle.velocity[2]:.2f}m/s")
        print(f"空速={vehicle.airspeed:.2f}m/s, 地速={vehicle.groundspeed:.2f}m/s")
        time.sleep(0.033333)
