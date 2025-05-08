# Setup and Usage Instructions for TMotor CAN Control

## 1. Bring up the CAN interface
Ensure the CAN interface is properly configured:

```bash
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 up
```

## 2. Activate the virtual environment

```bash
source Tmotor/bin/activate
```

## 3. Run the main control script

```bash
python mit_main.py
```

> ⚠️ If the script doesn't work, use a multimeter to verify the motor circuit is properly connected and powered.

## 4. Modify Temperature Threshold (Optional)
If the motor is responding and you want to adjust the thermal limit:

Edit this line in `mit_can.py`:

```python
temperature = 80
```

---
# 🔧 Setup and Usage Instructions for TMotor CAN Control

## 1. Bring up the CAN interface
Ensure the CAN interface is properly configured:

```bash
sudo ip link set can0 up type can bitrate 1000000
sudo ifconfig can0 up
```

## 2. Activate the virtual environment

```bash
source Tmotor/bin/activate
```

## 3. Run the main control script

```bash
python mit_main.py
```

> ⚠️ If the script doesn't work, use a multimeter to verify the motor circuit is properly connected and powered.

## 4. Modify Temperature Threshold (Optional)
If the motor is responding and you want to adjust the thermal limit:

Edit this line in `mit_can.py`:

```python
max_temp = 80
```

## 🔄 Code Changes Log

### File: `mit_main.py`

Replaced Greek letters with English equivalents for improved terminal readability in the `__str__` method.

**Before:**
```python
def __str__(self):
    return f"θ: {self.theta}, τ: {self.tau}, ω: {self.omega}"
```

**After:**
```python
 def __str__(self):
        """Prints the motor's device info and current"""
        return (
            self.device_info_string() +
            " | Position: {:.3f} rad".format(self.get_motor_angle_radians()) +
            " | Velocity: {:.3f} rad/s".format(self.get_motor_velocity_radians_per_second()) +
            " | Current: {:.3f} A".format(self.get_current_qaxis_amps()) +
            " | Torque: {:.3f} Nm".format(self.get_motor_torque_newton_meters())
        )
```

> ✅ This makes printed log messages more accessible and avoids encoding issues in some terminals.


