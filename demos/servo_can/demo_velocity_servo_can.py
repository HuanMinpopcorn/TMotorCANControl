from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from sys import path
path.append("/home/hipexo/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time
import numpy as np

target_vel = 0.2  # rad/s

with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1) as dev:
    dev.enter_velocity_control()

    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    for t in loop:
        # dev.velocity = target_vel
        dev.set_output_velocity_radians_per_second(target_vel)
        dev.update()

        actual_vel = dev.get_output_velocity_radians_per_second()
        pos_rad = dev.get_output_angle_radians()

        print(f"\r[t={t:.2f}s] Target vel: {target_vel:.2f} rad/s | Measured vel: {actual_vel:.2f} rad/s | Pos: {pos_rad:.2f} rad", end='')
            