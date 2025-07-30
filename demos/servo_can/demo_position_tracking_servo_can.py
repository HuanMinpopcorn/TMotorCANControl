from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from sys import path
path.append("/home/hipexo/HipExo/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time
import numpy as np
import csv
import matplotlib.pyplot as plt

# [LOG]]changed the parameter for the motor and overflow for bites 
# Create log containers
log_data = {
    "time": [],
    "desired_position": [],
    "actual_position": [],
    "position_error": [],
    "tracking_coefficient": []
}

with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1) as dev:
    # dev.update()
    
    dev.set_zero_position()
    dev.enter_position_control()
    dev.update()
    time.sleep(1.5)
    loop = SoftRealtimeLoop(dt=0.001, report=True, fade=0.0)
    for t in loop:

        desired_position = 0.1 * np.sin(t * 2 * np.pi / 2) # Example desired position in radians
        # desired_position = 3.1415926 
        dev.set_output_angle_radians(pos=desired_position)
   
        actual_position = dev.get_output_angle_radians() 
        dev.update()
       
       
        position_error = desired_position - actual_position
        tracking_coeff = actual_position / desired_position if abs(desired_position) > 1e-5 else 0.0

        # Log data
        log_data["time"].append(t)
        log_data["desired_position"].append(desired_position)
        log_data["actual_position"].append(actual_position)
        log_data["position_error"].append(position_error)


        # Print live tracking information
        # print(f"t={t:.3f}s | Desired: {desired_position:.3f} rad | Actual: {actual_position:.3f} rad | Error: {position_error:.4f} rad" , end='\r')

        if t > 10:
            break

# Plotting tracking curve
plt.figure()
plt.plot(log_data["time"], log_data["desired_position"], label="Desired Position")
plt.plot(log_data["time"], log_data["actual_position"], label="Actual Position")
plt.plot(log_data["time"], log_data["position_error"], label="Position Error", linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("Position / Coefficient")
plt.title("Position Tracking with Error and Coefficient")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()