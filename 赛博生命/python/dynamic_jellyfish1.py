import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 设置图形和坐标轴
fig, ax = plt.subplots(figsize=(9, 9), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_aspect('equal')
ax.axis('off')  # 关闭坐标轴刻度和标签

# 初始化散点对象
scat = ax.scatter([], [], s=1, c='white', alpha=0.4, marker='o', edgecolors='none')

# 预计算一些常量和数据
i = np.arange(10000)  # 使用 10000 个点
x = np.mod(i, 200)
y = i / 43.0
k = 5 * np.cos(x / 14.0) * np.cos(y / 30.0)
e = y / 8.0 - 13.0
d = (k**2 + e**2) / 59.0 + 4.0
a = np.arctan2(k, e) # 使用 np.arctan2 替代 atan2

# 动画更新函数
def update(frame):
    t = frame * np.pi / 10  # 计算当前时间 t

    # 计算 q 和 c
    q = 60 - 3 * np.sin(a * e) + k * (3 + 4 / d * np.sin(d**2 - t * 2))
    c = d / 2 + e / 99 - t / 18

    # 计算新的 X 和 Y 数据
    new_x = q * np.sin(c) + 200
    new_y = (q + d * 9) * np.cos(c) + 200

    # 计算动态颜色，使用柔和的色彩变化
    colors = np.array([[0.2 + 0.3 * np.sin(x_i/40 + t * 0.5), 
                       0.4 + 0.4 * np.cos(y_i/30 - t * 0.8), 
                       0.6 + 0.5 * np.sin((x_i + y_i)/50 + t * 0.6)] for x_i, y_i in zip(new_x, new_y)])
    # 确保颜色值在0-1范围内
    colors = np.clip(colors, 0, 1)
    scat.set_facecolors(colors)

    # 更新散点的数据
    scat.set_offsets(np.column_stack((new_x, new_y)))

    return scat,

# 创建动画
# interval: 每帧之间的间隔（毫秒），值越小动画越快
# blit: 优化绘制，只重绘变化的部分（可能在某些后端不工作）
ani = FuncAnimation(fig, update, interval=50, blit=False, cache_frame_data=False) # interval 50ms 大约 20 FPS

# 显示图形窗口
plt.tight_layout()
plt.show()

# 注意：在某些环境中，plt.show() 会阻塞程序，动画会在此处运行
# 在交互式环境（如 Jupyter Notebook）中，可能需要特殊的后端支持




