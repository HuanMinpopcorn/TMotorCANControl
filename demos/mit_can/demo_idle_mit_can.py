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

def read_only(dev):
    dev.set_zero_position()
    time.sleep(1.5) # wait for the motor to zero (~1 second)
    
    print("Starting read only demo. Press ctrl+C to quit.")
    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    
    for t in loop:
        dev.update()
        print("\r" + str(dev), end='')


if __name__ == '__main__':
<<<<<<< HEAD
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID) as dev:
=======
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID,max_mosfett_temp=80) as dev:
>>>>>>> 1fb50f0 (first commited change the original file)
        read_only(dev)