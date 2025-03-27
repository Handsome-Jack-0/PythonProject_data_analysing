import serial
import time
import numpy as np
import colorsys
import random
import struct
from scipy.signal import welch
import matplotlib.pyplot as plt

# 初始化串口
ser = serial.Serial('COM5', 115200, timeout=1)

# 自动校准环境噪声
def calibrate_noise(duration=3):
    print("正在校准环境噪声，请保持安静...")
    samples = []
    start = time.time()
    while time.time() - start < duration:
        raw_data = ser.readline().decode().strip()
        if raw_data:
            samples.append(int(raw_data))
    baseline = np.mean(samples) + 2 * np.std(samples)
    print(f"校准完成！动态阈值设置为: {baseline}")
    return baseline

NOISE_THRESHOLD = calibrate_noise()

# 单色LED - 脉冲呼吸效果
def pulse_effect(sound_value):
    # 基础亮度映射（过滤低强度噪声）
    if sound_value < NOISE_THRESHOLD:
        return 0
    base_brightness = int(np.interp(sound_value, [NOISE_THRESHOLD, 1023], [50, 255]))

    # 呼吸波形参数
    phase = time.time() * 4  # 控制呼吸速度（4Hz）
    pulse = int(np.sin(phase) * 100)  # 呼吸幅度±100

    # 合成亮度并限制范围
    return np.clip(base_brightness + pulse, 0, 255)

# RGB LED - 节拍检测增强版
class BeatDetector:
    def __init__(self):
        self.energy_history = []
        self.threshold = 0.5

    def update(self, buffer):
        energy = np.mean(np.abs(buffer))
        self.energy_history.append(energy)
        if len(self.energy_history) > 30:  # 保留30帧历史数据
            self.energy_history.pop(0)

        # 动态阈值 = 历史平均能量 * 系数
        dynamic_thresh = np.mean(self.energy_history) * 2.0
        return energy > dynamic_thresh

beat_detector = BeatDetector()

# RGB LED - HSV颜色渐变生成器
def color_generator(sound_value):
    hue = (time.time() * 0.3) % 1.0  # 色相每3秒循环一次
    saturation = 1.0
    value = np.interp(sound_value, [200, 800], [0.3, 1.0])
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)

# 节拍检测 - 频带能量分析
def analyze_energy(buffer, fs=5000):
    freqs, psd = welch(buffer, fs=fs, nperseg=64)
    bass_energy = np.sum(psd[(freqs >= 50) & (freqs < 200)])
    return bass_energy > 0.5  # 低音能量阈值

# 实时波形显示
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])

def update_plot(data):
    line.set_ydata(data)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.flush_events()

# 主循环
try:
    buffer = []
    while True:
        raw_data = ser.readline().decode().strip()
        if raw_data:
            sound = int(raw_data)
            buffer.append(sound)

            # 每20ms处理一次（约50Hz）
            if len(buffer) >= 10:
                # 单色LED处理
                brightness = pulse_effect(sound)
                # 这里可以根据需求决定是否使用二进制传输
                ser.write(f"{brightness}\n".encode())

                # RGB LED处理
                # 节拍检测
                if beat_detector.update(buffer):
                    # 节拍时切换随机颜色
                    hue_jump = random.uniform(0.1, 0.3)
                    # 白色闪光（二进制传输示例）
                    ser.write(struct.pack('BBB', 255, 255, 255))
                    time.sleep(0.03)

                # 常态颜色渐变
                r, g, b = color_generator(np.median(buffer))
                # 二进制传输RGB值
                ser.write(struct.pack('BBB', r, g, b))

                # 频带能量分析
                if analyze_energy(buffer):
                    print("检测到低频能量峰值！")

                # 实时波形显示
                update_plot(buffer)

                buffer = []

except KeyboardInterrupt:
    ser.close()