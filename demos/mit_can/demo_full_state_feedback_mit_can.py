from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from NeuroLocoMiddleware.SysID import Chirp
import numpy as np
import time
from TMotorCANControl.mit_can import TMotorManager_mit_can

# CHANGE THESE TO MATCH YOUR DEVICE!
<<<<<<< HEAD
Type = 'AK80-9'
=======
Type = 'AK70-10'
>>>>>>> 1fb50f0 (first commited change the original file)
ID = 1

def full_state_feedback(dev):
    dev.set_zero_position() # has a delay!
<<<<<<< HEAD
    time.sleep(1.5)
=======
    time.sleep(0.1)
>>>>>>> 1fb50f0 (first commited change the original file)
    dev.set_impedance_gains_real_unit_full_state_feedback(K=10,B=1)
    chirp = Chirp(250, 200, 0.5)

    print("Starting full state feedback demo. Press ctrl+C to quit.")

<<<<<<< HEAD
    loop = SoftRealtimeLoop(dt = 0.001, report=True, fade=0)
=======
    loop = SoftRealtimeLoop(dt = 0.005, report=True, fade=0)
>>>>>>> 1fb50f0 (first commited change the original file)
    amp = 1.0
  
    for t in loop:
        dev.update()
<<<<<<< HEAD
=======
        theta = dev._motor_state.position 
        omega = dev._motor_state.velocity
        current = dev._motor_state.current
        print(f"[{t:.3f}s] θ: {theta:.3f} rad | ω: {omega:.3f} rad/s | i: {current:.2f} A")

>>>>>>> 1fb50f0 (first commited change the original file)
        if t < 1.0:
            dev.torque = 0.0
            dev.position = 0.0
        else:
            des_τ = loop.fade*amp*chirp.next(t)*3/3.7
            dev.torque = des_τ
            dev.position = (np.pi/2)*int(t)

    del loop

if __name__ == '__main__':
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID) as dev:
        full_state_feedback(dev)