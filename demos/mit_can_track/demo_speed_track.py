from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
import time
import matplotlib.pyplot as plt
from TMotorCANControl.mit_can import TMotorManager_mit_can
import numpy as np

# CHANGE THESE TO MATCH YOUR DEVICE
Type = 'AK70-10'
ID = 1

def sine_speed_tracking(dev):
    dev.set_zero_position()
    time.sleep(3.0)  # wait for motor to zero
    dev.set_speed_gains(kd=3.0)

    print("Starting sine wave speed tracking. Press ctrl+C to stop.")

    # Sine wave parameters
    A = 1     # Amplitude (rad/s)
    f = 1.0      # Frequency (Hz)

    # Logging
    times = []
    desired_velocities = []
    actual_velocities = []

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    desired_line, = ax.plot([], [], label="Desired Velocity (rad/s)")
    actual_line, = ax.plot([], [], label="Actual Velocity (rad/s)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (rad/s)")
    ax.set_title("Real-Time Velocity Tracking")
    ax.legend()
    ax.grid(True)

    loop = SoftRealtimeLoop(dt=0.001, report=True, fade=0)
    for t in loop:
        dev.update()
        desired_velocity = A * np.sin(2 * np.pi * f * t)
        dev.velocity = desired_velocity

        # Logging
        times.append(t)
        desired_velocities.append(desired_velocity)
        actual_velocities.append(dev._motor_state.velocity)

        # Update plot every 10 ms (optional tweak)
        if len(times) % 10 == 0:
            desired_line.set_data(times, desired_velocities)
            actual_line.set_data(times, actual_velocities)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.001)

    del loop
    plt.ioff()
    plt.show()

if __name__ == '__main__':
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID,max_mosfett_temp=80) as dev:
        sine_speed_tracking(dev)
