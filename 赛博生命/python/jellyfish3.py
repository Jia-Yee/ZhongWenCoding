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

# 预计算一些常量和数据 (在循环外计算不变的部分)
i = np.arange(10000)  # 使用 10000 个点
x = np.mod(i, 200).astype(float)
y = i / 55.0
k = 9 * np.cos(x / 8.0)
e = y / 8.0 - 12.5

# 动画更新函数
def update(frame):
    t = frame * np.pi / 120  # 计算当前时间 t

    # 计算 d
    d = (k**2 + e**2) / 99.0 + np.sin(t) / 6.0 + 0.5

    # 计算 atan2 部分
    atan2_val = np.arctan2(k, e)

    # 计算 q 和 c
    q = 99 - e * np.sin(atan2_val * 7) / d + k * (3 + np.cos(d**2 - t) * 2)
    c = d / 2.0 + e / 69.0 - t / 16.0

    # 计算新的 X 和 Y 数据
    new_x = q * np.sin(c) + 200
    new_y = (q + 19 * d) * np.cos(c) + 200

    # 更新散点的数据
    scat.set_offsets(np.column_stack((new_x, new_y)))

    return scat,

# 创建动画
ani = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False) # interval 20ms 大约 50 FPS

# 显示图形窗口
plt.tight_layout()
plt.show()

# 注意：在某些环境中，plt.show() 会阻塞程序，动画会在此处运行
# 在交互式环境（如 Jupyter Notebook）中，可能需要特殊的后端支持




