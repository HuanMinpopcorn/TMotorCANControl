from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
# try:
#      from TMotorCANControl.TMotorManager import TMotorManager
# except ModuleNotFoundError:
from sys import path
path.append("/home/hipexo/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time
import numpy as np


with TMotorManager_servo_can(motor_type='AK70-10', motor_ID=1, CSV_file="logs.csv") as dev:
    dev.enter_position_control()
    loop = SoftRealtimeLoop(dt=0.01, report=True, fade=0.0)
    dev.set_zero_position()
    
    for t in loop:
        dev.position = 3.14159/100*2
        # dev._command.position = 0.2
        dev.update()
        print("\r" + str(dev),end='')
