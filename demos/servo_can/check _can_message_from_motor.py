import can
import struct
import time

channel = 'can0'
motor_id = 93
bus = can.interface.Bus(channel=channel, bustype='socketcan')

def parse_feedback(msg):
    data = msg.data
    pos_raw = struct.unpack('>h', bytes(data[0:2]))[0]  # int16
    vel_raw = struct.unpack('>h', bytes(data[2:4]))[0]  # int16
    cur_raw = struct.unpack('>h', bytes(data[4:6]))[0]  # int16
    temp = data[6]
    error = data[7]

    pos = pos_raw * 0.1        # deg
    vel = vel_raw * 10.0       # deg/s
    cur = cur_raw * 0.01       # A

    return pos, vel, cur, temp, error

def read_feedback(timeout=0.1):
    msg = bus.recv(timeout)
    if msg or msg.arbitration_id == hex(motor_id):
        return parse_feedback(msg)
    return None

def send_velocity_command(velocity_deg_s):
    vel_int = int(velocity_deg_s / 10.0)
    vel_bytes = vel_int.to_bytes(2, byteorder='big', signed=True)
    cmd = bytearray([0xA2]) + vel_bytes + bytearray(5)
    msg = can.Message(arbitration_id=0x140 + motor_id, data=cmd, is_extended_id=False)
    bus.send(msg)

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

print("Reading feedback and sending dummy velocity commands...")
try:
    enable_motor()
    while True:
        feedback = read_feedback()
        if feedback:
            pos, vel, cur, temp, err = feedback
            print(f"Position: {pos:.1f} deg | Velocity: {vel:.1f} deg/s | Current: {cur:.3f} A | Temp: {temp} C | Error: {err}")

        # send_velocity_comsmand(velocity_deg_s=0.01)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Stopping motor...")
    stop_motor()
