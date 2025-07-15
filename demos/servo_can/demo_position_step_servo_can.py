from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
# try:
#      from TMotorCANControl.TMotorManager import TMotorManager
# except ModuleNotFoundError:
from sys import path
path.append("/home/hipexo/TMotorCANControl/src/")
from TMotorCANControl.servo_can import TMotorManager_servo_can
import time
import numpy as np


with TMotorManager_servo_can(motor_type='AK80-9', motor_ID=93, CSV_file="logs.csv") as dev:
    dev.enter_position_control()
    loop = SoftRealtimeLoop(dt=1, report=True, fade=0.0)
    dev.set_zero_position()
    
    for t in loop:
        # dev.position = 1
        dev._command.position = 0.1 
        dev.update()
        print("\r" + str(dev),end='')
