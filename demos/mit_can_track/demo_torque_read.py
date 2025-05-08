import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from TMotorCANControl.mit_can import TMotorManager_mit_can
from NeuroLocoMiddleware.SoftRealtimeLoop import SoftRealtimeLoop
from NeuroLocoMiddleware.SysID import Chirp

# 设置电机
Type = 'AK70-10'
ID = 2
kt = 0.095  # 力矩常数（Nm/A）

# 记录数据
times = []
desired_torques = []
actual_torques = []

fig, ax = plt.subplots()
line_des, = ax.plot([], [], label='Desired Torque (Nm)')
line_act, = ax.plot([], [], label='Actual Torque (Nm)')
ax.set_xlim(0, 10)
ax.set_ylim(-2, 2)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Torque (Nm)")
ax.set_title("Torque Tracking")
ax.grid(True)
ax.legend()

def init():
    line_des.set_data([], [])
    line_act.set_data([], [])
    return line_des, line_act

def update_plot(frame):
    if not times:
        return line_des, line_act
    ax.set_xlim(max(0, times[-1] - 10), times[-1] + 1)
    line_des.set_data(times, desired_torques)
    line_act.set_data(times, actual_torques)
    return line_des, line_act

def full_state_feedback(dev):
    dev.set_zero_position()
    time.sleep(1.0)
    dev.set_impedance_gains_real_unit_full_state_feedback(K=10, B=1)

    chirp = Chirp(250, 200, 0.5)
    print("Starting full state feedback with torque tracking...")

    loop = SoftRealtimeLoop(dt=0.001, report=False)
    amp = 1.0
    t_start = time.time()

    def control_loop():
        for t in loop:
            now = time.time() - t_start
            dev.update()

            current = dev._motor_state.current
            actual_torque = current * kt

            if t < 1.0:
                des_τ = 0.0
                dev.torque = 0.0
                dev.position = 0.0
            else:
                des_τ = loop.fade * amp * chirp.next(t) * 3 / 3.7
                dev.torque = des_τ
                dev.position = (np.pi / 2) * int(t)

            # 存储数据
            times.append(now)
            desired_torques.append(des_τ)
            actual_torques.append(actual_torque)

            # 如果图被关了就退出控制循环
            if not plt.fignum_exists(fig.number):
                break

    import threading
    threading.Thread(target=control_loop, daemon=True).start()

    ani = FuncAnimation(fig, update_plot, init_func=init, blit=True, interval=50)
    plt.show()

if __name__ == '__main__':
    with TMotorManager_mit_can(motor_type=Type, motor_ID=ID) as dev:
        full_state_feedback(dev)
