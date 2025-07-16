import can
import struct
import time
import numpy as np
import matplotlib.pyplot as plt
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop

# Setup CAN interface
channel = 'can0'
motor_id = 93
bus = can.interface.Bus(channel=channel, interface='socketcan')

def parse_feedback(msg):
    data = msg.data
    if len(data) == 8:
        pos_raw = struct.unpack('>h', bytes(data[0:2]))[0]  # int16
        vel_raw = struct.unpack('>h', bytes(data[2:4]))[0]  # int16
        cur_raw = struct.unpack('>h', bytes(data[4:6]))[0]  # int16
        temp = data[6]
        error = data[7]

        pos = pos_raw * 0.1        # deg
        vel = vel_raw * 10.0       # deg/s
        cur = cur_raw * 0.01       # A

        return pos, vel, cur, temp, error
    elif len(data) == 6:
        pos_raw = struct.unpack('>i', bytes(data[2:6]))[0]  # int32
        pos = pos_raw / 1000.0     # deg
        return pos, None, None, None, None
    return None

def read_feedback(timeout=0.01):
    msg = bus.recv(timeout)
    if msg:
        return parse_feedback(msg)
    return None

def enable_motor():
    cmd = bytearray([0x06] + [0x00]*7)
    msg = can.Message(arbitration_id=0x140 + motor_id, data=cmd, is_extended_id=False)
    bus.send(msg)
    print("Motor enabled.")
    time.sleep(0.5)

def stop_motor():
    cmd = bytearray([0x81] + [0x00]*7)
    msg = can.Message(arbitration_id=0x140 + motor_id, data=cmd, is_extended_id=False)
    bus.send(msg)
    print("Motor stopped.")

def send_position_command(position_deg):
    pos_int = int(position_deg * 10000.0)  # as per CubeMars CAN_PACKET_SET_POS convention
    pos_bytes = pos_int.to_bytes(4, byteorder='big', signed=True)
    cmd = bytearray([0x02, 0x05, 0x16, 0x00]) + pos_bytes
    checksum = (256 - sum(cmd[1:])) & 0xFF
    cmd.append(checksum)
    cmd.append(0x03)
    msg = can.Message(arbitration_id=(motor_id | (0x00 << 8)), data=cmd, is_extended_id=True)
    bus.send(msg)

def set_origin(mode=0):
    # mode: 0 for temporary, 1 for permanent
    cmd = bytearray([mode]) + bytearray(7)
    msg = can.Message(arbitration_id=(motor_id | (0x0B << 8)), data=cmd, is_extended_id=True)
    bus.send(msg)
    print(f"Origin set with mode {mode}.")

# Create log containers
log_data = {
    "time": [],
    "desired_position": [],
    "actual_position": [],
    "position_error": [],
    "tracking_coefficient": []
}

print("Starting CAN-based position tracking using CubeMars format...")

try:
    enable_motor()
    set_origin(mode=0)  # Temporary origin

    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    t_start = time.time()

    for t in loop:
        elapsed = time.time() - t_start
        desired_position_rad = 0.17 * np.sin(elapsed)
        desired_position_deg = desired_position_rad * 180 / np.pi
        print(2)
        send_position_command(desired_position_deg)

        feedback = read_feedback()
        if feedback:
            if feedback[1] is not None:
                pos_deg, vel_deg_s, cur_a, temp_c, err = feedback
            else:
                pos_deg = feedback[0]
            actual_position_rad = pos_deg * np.pi / 180
        else:
            actual_position_rad = 0.0

        position_error = desired_position_rad - actual_position_rad
        tracking_coeff = actual_position_rad / desired_position_rad if abs(desired_position_rad) > 1e-5 else 0.0

        log_data["time"].append(elapsed)
        log_data["desired_position"].append(desired_position_rad)
        log_data["actual_position"].append(actual_position_rad)
        log_data["position_error"].append(position_error)
        log_data["tracking_coefficient"].append(tracking_coeff)

        print(f"t={elapsed:.3f}s | Desired: {desired_position_rad:.3f} rad | Actual: {actual_position_rad:.3f} rad", end='\r')

        if elapsed > 10:
            break

except KeyboardInterrupt:
    print("\nInterrupted.")

finally:
    stop_motor()

    plt.figure()
    plt.plot(log_data["time"], log_data["desired_position"], label="Desired Position")
    plt.plot(log_data["time"], log_data["actual_position"], label="Actual Position")
    plt.plot(log_data["time"], log_data["position_error"], label="Position Error", linestyle="--")
    plt.xlabel("Time (s)")
    plt.ylabel("Position (rad)")
    plt.title("Position Tracking with CubeMars Protocol")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
