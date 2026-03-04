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

# 预计算一些常量和数据 (在循环外计算不变的部分)
i = np.arange(int(4e4))  # 使用 40000 个点
x = np.mod(i, 200).astype(float)
y = i / 200.0
k = x / 8.0 - 12.5
e = y / 8.0 - 12.5
o = (k**2 + e**2) / 169.0
d_base = 0.5 + 5.0 * np.cos(o)

# 初始化散点对象
# 初始颜色数据可以是任意的，因为 update 函数会不断更新
scat = ax.scatter([], [], s=1, c='white', alpha=0.4, marker='o', edgecolors='none')

# 动画更新函数
def update(frame):
    t = frame * np.pi / 30  # 计算当前时间 t

    # 重新计算随时间变化的部分
    d = d_base # d_base 已经计算好，d 在这个动画中不随 t 变化，所以直接用 d_base
    sin_term = np.sin(d * 2 + o + t)
    cos_term = np.cos(d * 3 + o * 9 + t)

    # 计算新的 X 和 Y 数据
    new_x = x + d * k * sin_term + e * np.cos(e + t) + 100
    new_y = y / 4.0 - o * 135 + d * 6.0 * cos_term + 275

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

# 重新初始化scat以配合set_array
scat = ax.scatter([], [], s=1, marker='o', edgecolors='none', alpha=0.4, cmap='gray', vmin=0, vmax=1)

# 创建动画
ani = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False) # interval 20ms 大约 50 FPS

# 显示图形窗口
plt.tight_layout()
plt.show()

# 注意：在某些环境中，plt.show() 会阻塞程序，动画会在此处运行
# 在交互式环境（如 Jupyter Notebook）中，可能需要特殊的后端支持




