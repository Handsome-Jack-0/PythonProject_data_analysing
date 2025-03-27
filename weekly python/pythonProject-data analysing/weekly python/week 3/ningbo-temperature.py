import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
colors = sns.color_palette("Set2")


# 绘制温度趋势图
def plot_temperature(ax, df):
    ax.plot(df['日期'], df['高温'], marker='o', color=colors[0], label='高温')
    ax.plot(df['日期'], df['低温'], marker='o', color=colors[1], label='低温')
    ax.fill_between(df['日期'], df['高温'], df['低温'], color=colors[2], alpha=0.3)
    ax.set_title('温度趋势（℃）')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m月'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.grid(linestyle='--', alpha=0.5)
    ax.legend()


# 绘制降雨量柱状图
def plot_rainfall(ax, df):
    bars = ax.bar(df['日期'], df['总降雨'], color=colors[3], alpha=0.7, label='降雨量')
    ax.plot(df['日期'], df['总降雨'], color=colors[4], marker='o', linestyle='--', label='趋势线')
    ax.set_title('月总降雨量（mm）')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m月'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{height}mm',
                ha='center', va='bottom', fontsize=8)


# 绘制能见度与风速双轴图
def plot_visibility_wind(ax, df):
    color = colors[5]
    ax.set_xlabel('月份')
    ax.set_ylabel('能见度 (km)', color=color)
    ax.plot(df['日期'], df['能见度'], color=color, marker='^', linestyle='--')
    ax.tick_params(axis='y', labelcolor=color)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    ax2 = ax.twinx()
    color = colors[6]
    ax2.set_ylabel('风速 (km/h)', color=color)
    ax2.plot(df['日期'], df['风速'], color=color, marker='s', linestyle='-.')
    ax2.tick_params(axis='y', labelcolor=color)
    ax.set_title('能见度与风速关系')


# 绘制空气质量玫瑰图
def plot_air_quality(ax, df):
    categories = df['空气质量'].unique()
    counts = [df['空气质量'].value_counts().get(category, 0) for category in categories]
    theta = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    width = np.pi / len(categories)

    rose_colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))
    bars = ax.bar(theta, counts, width=width, align='edge',
                  color=rose_colors, alpha=0.7, edgecolor='black')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_xticks(theta)
    ax.set_xticklabels(categories)
    ax.set_title('空气质量分布', y=1.08)


# 绘制温雨复合图
def plot_temp_rainfall(ax, df):
    ax.plot(df['日期'], df['高温'], marker='o', color=colors[0], label='高温')
    ax.plot(df['日期'], df['低温'], marker='o', color=colors[1], label='低温')
    ax.fill_between(df['日期'], df['高温'], df['低温'], color=colors[2], alpha=0.3)
    ax.set_ylabel('温度 (℃)', color=colors[1])
    ax.tick_params(axis='y', labelcolor=colors[1])
    ax.legend(loc='upper left')

    ax2 = ax.twinx()
    ax2.bar(df['日期'], df['总降雨'], color=colors[3], alpha=0.3, label='降雨量')
    ax2.set_ylabel('降雨量 (mm)', color=colors[4])
    ax2.tick_params(axis='y', labelcolor=colors[4])
    ax2.legend(loc='upper right')
    ax.set_title('温度与降雨量复合分析')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m月'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())


# 创建数据框
data = {
    "月份": [f"2024年{str(i).zfill(2)}月" for i in range(1, 13)],
    "高温": [12, 11, 19, 22, 26, 28, 36, 37, 31, 24, 19, 12],
    "低温": [2, 4, 7, 14, 16, 21, 26, 26, 24, 17, 12, 3],
    "空气": ["76 良", "48 优", "52 优", "40 优", "37 优", "31 优",
             "31 优", "38 优", "28 优", "36 优", "41 优", "73 优"],
    "能见度": [13.6, 13.7, 8.5, 7.4, 14.6, 9.9, 16.5, 21, 18, 16.6, 15.7, 14.9],
    "风速": [10.3, 11.7, 9.1, 8.5, 9.6, 6.6, 13.5, 8.6, 9.9, 11, 10.6, 10],
    "总降雨": [23.9, 40.6, 11.8, 173.6, 10.8, 97.2, 36.8, 33.7, 21.1, 164, 53.7, 34.8]
}

df = pd.DataFrame(data)
df['日期'] = pd.to_datetime(df['月份'].str.replace('年', '-').str.replace('月', ''), format='%Y-%m')
df[['AQI', '空气质量']] = df['空气'].str.split(' ', expand=True)
df['AQI'] = pd.to_numeric(df['AQI'], errors='coerce').fillna(0).astype(int)

# 创建画布
fig = plt.figure(figsize=(18, 12), dpi=100)
fig.suptitle('宁波2024年气象数据可视化分析', fontsize=16, y=1.02)

# 温度趋势图
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2)
plot_temperature(ax1, df)

# 降雨量柱状图
ax2 = plt.subplot2grid((3, 3), (0, 2))
plot_rainfall(ax2, df)

# 能见度与风速双轴图
ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
plot_visibility_wind(ax3, df)

# 空气质量玫瑰图
ax4 = plt.subplot2grid((3, 3), (1, 2), polar=True)
plot_air_quality(ax4, df)

# 温雨复合图
ax5 = plt.subplot2grid((3, 3), (2, 0), colspan=3)
plot_temp_rainfall(ax5, df)

# 调整布局
plt.tight_layout()

# 保存图片
try:
    plt.savefig('ningbo_weather_analysis.jpg', bbox_inches='tight', dpi=300, facecolor='white')
    plt.savefig('ningbo_weather_analysis.pdf', bbox_inches='tight', dpi=300, facecolor='white')
except IOError as e:
    print(f"保存失败: {e}")

plt.show()