from dronekit import connect, Command , VehicleMode
from pymavlink import mavutil  # 正确导入方式

def add_mission(vehicle):
    cmds = vehicle.commands
    cmds.clear()

    # 1. 起飞命令
    cmds.add(Command(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,  # 使用标准命令
        0, 0,
        0, 0, 0, 0,  # param1~param4
        0, 0, 1       # 高度1米
    ))

    # 2. 前飞10米（使用MAV_FRAME_BODY_OFFSET_NED）
    cmds.add(Command(
        0, 0, 0,
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,  # 正确命令类型
        0, 0,
        0,    # 停留时间（秒）
        5,    # 接受半径（米）
        0, 0, # 参数3~4
        10,   # x（前向距离，米）
        0,    # y（右向距离，米）
        0     # z（高度，米）
    ))

    
    cmds.upload()
    print("任务上传成功")

# 连接飞控（强制启用MISSION_ITEM_INT消息格式）
# 2. 手动设置 MAVLink 协议版本
vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
vehicle._master.mav.mission_count_send(
    vehicle.target_system,
    vehicle.target_component,
    0,  # mission_type (0:Mission)
    0   # 使用 MISSION_ITEM_INT
)

msg = vehicle.message_factory.set_position_target_local_ned_encode(
    0,       # 时间戳
    0, 0,    # 目标系统ID和目标组件ID
    mavutil.mavlink.MAV_FRAME_BODY_NED,  # 坐标系
    0b0000111111000111, # 控制速度的位掩码
    0, 0, 0, # 位置参数（忽略）
    0, -left_speed, 0, # 速度参数（X,Y,Z）- Y为负表示向左
    0, 0, 0, # 加速度参数（忽略）
    0, 0)    # 偏航参数（忽略）
add_mission(vehicle)
vehicle.mode = VehicleMode("AUTO")
vehicle.armed   = True