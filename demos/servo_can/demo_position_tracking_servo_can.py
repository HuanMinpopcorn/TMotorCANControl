from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from sys import path
path.append("/home/hipexo/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time
import numpy as np
import csv
import matplotlib.pyplot as plt



# Create log containers
log_data = {
    "time": [],
    "desired_position": [],
    "actual_position": []
}

with TMotorManager_servo_can(motor_type='AK80-9', motor_ID=93) as dev:
    dev.update()
    time.sleep(1.5)
    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    dev.set_zero_position()
    dev.enter_position_control()
    time.sleep(1.5)

    for t in loop:
        desired_position = 0.1 * np.sin(t)  # rad
        dev._command.position = desired_position
        dev.update()

        # Log data
        log_data["time"].append(t)
        log_data["desired_position"].append(desired_position)
        log_data["actual_position"].append(dev._motor_state.position)

        # Print live tracking information
        print(f"t={t:.3f}s | Desired: {desired_position:.3f} rad | Actual: {dev._motor_state.position:.3f} rad", end='\r')

        if t > 10:
            break

# Plotting tracking curve
plt.figure()
plt.plot(log_data["time"], log_data["desired_position"], label="Desired Position")
plt.plot(log_data["time"], log_data["actual_position"], label="Actual Position")
plt.xlabel("Time (s)")
plt.ylabel("Position (rad)")
plt.title("Position Tracking")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()