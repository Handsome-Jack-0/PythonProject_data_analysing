import serial
import time
import numpy as np
import colorsys
import random  # 新增导入

ser = serial.Serial('COM3', 115200, timeout=1)


# ------------------ 节拍检测增强版 ------------------
class BeatDetector:
    def __init__(self, threshold_coeff=2.0):
        self.energy_history = []
        self.threshold_coeff = threshold_coeff

    def update(self, buffer):
        energy = np.mean(np.abs(buffer))
        self.energy_history.append(energy)
        if len(self.energy_history) > 30:  # 保留30帧历史数据
            self.energy_history.pop(0)

        # 动态阈值 = 历史平均能量 * 系数
        if self.energy_history:  # 避免空列表错误
            dynamic_thresh = np.mean(self.energy_history) * self.threshold_coeff
            return energy > dynamic_thresh
        return False  # 初始无数据时不触发


beat_detector = BeatDetector(threshold_coeff=2.5)  # 可调整系数


# ------------------ HSV颜色渐变生成器 ------------------
def color_generator(sound_value):
    hue = (time.time() * 0.3) % 1.0  # 色相每3秒循环一次
    saturation = 1.0
    value = np.interp(sound_value, [200, 800], [0.3, 1.0])
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)


# ------------------ 主循环 ------------------
buffer = []
try:
    while True:
        raw_data = ser.readline().decode().strip()
        if raw_data:
            sound = int(raw_data)
            buffer.append(sound)

            # 每20ms处理一次（约50Hz）
            if len(buffer) >= 10:
                # 节拍检测
                if beat_detector.update(buffer):
                    # 白色闪光 + 随机颜色切换
                    ser.write(f"255,255,255\n".encode())
                    time.sleep(0.03)
                    new_hue = random.uniform(0, 1)  # 随机色相
                    r, g, b = colorsys.hsv_to_rgb(new_hue, 1.0, 1.0)
                    ser.write(f"{int(r * 255)},{int(g * 255)},{int(b * 255)}\n".encode())

                # 常态颜色渐变
                r, g, b = color_generator(np.median(buffer))
                ser.write(f"{r},{g},{b}\n".encode())
                buffer = []

except KeyboardInterrupt:
    ser.close()