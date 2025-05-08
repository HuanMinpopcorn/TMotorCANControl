from TMotorCANControl.mit_can import TMotorManager_mit_can

<<<<<<< HEAD
# CHANGE THESE TO MATCH YOUR DEVICE!
Type = 'AK80-9'
=======

# bring the cano properly 
# sudo ip link set can0 up type can bitrate 1000000
# sudo ifconfig can0 up

# source the venv
# source Tmotor/bin/activate 

# run this file 
# if doesnt work, using mutimeter to check the circuit. 
# CHANGE THESE TO MATCH YOUR DEVICE!
Type = 'AK70-10'
>>>>>>> 1fb50f0 (first commited change the original file)
ID = 1

with TMotorManager_mit_can(motor_type=Type, motor_ID=ID) as dev:
    if dev.check_can_connection():
        print("\nmotor is successfully connected!\n")
    else:
        print("\nmotor not connected. Check dev power, network wiring, and CAN bus connection.\n")
    