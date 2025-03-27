import serial
import time
import numpy as np

# 初始化串口
ser = serial.Serial('COM5', 115200, timeout=1)


# ------------------ 自动校准环境噪声 ------------------
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


# ------------------ 动态呼吸效果 ------------------
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


# ------------------ 主循环 ------------------
try:
    while True:
        raw_data = ser.readline().decode().strip()
        if raw_data:
            sound = int(raw_data)
            brightness = pulse_effect(sound)
            ser.write(f"{brightness}\n".encode())

except KeyboardInterrupt:
    ser.close()