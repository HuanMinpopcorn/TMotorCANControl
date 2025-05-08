from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
import time
from TMotorCANControl.mit_can import TMotorManager_mit_can

# CHANGE THESE TO MATCH YOUR DEVICE!
<<<<<<< HEAD
Type = 'AK80-9'
=======
Type = 'AK70-10'
>>>>>>> 1fb50f0 (first commited change the original file)
ID = 1

def speed_step(dev):
    dev.set_zero_position()
    time.sleep(1.5) # wait for the motor to zero (~1 second)
    dev.set_speed_gains(kd=3.0)
    
    print("Starting speed step demo. Press ctrl+C to quit.")
    loop = SoftRealtimeLoop(dt = 0.01, report=True, fade=0)
    for t in loop:
        dev.update()
        if t < 1.0:
            dev.velocity = 0.0
        else:
<<<<<<< HEAD
            dev.velocity = 1.0
=======
            dev.velocity = 0.2
>>>>>>> 1fb50f0 (first commited change the original file)
            
    del loop

if __name__ == '__main__':
<<<<<<< HEAD
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID) as dev:
=======
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID, max_mosfett_temp=80) as dev:
>>>>>>> 1fb50f0 (first commited change the original file)
        speed_step(dev)