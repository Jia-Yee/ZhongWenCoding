import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# 设置图形和坐标轴
fig, ax = plt.subplots(figsize=(9, 9), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_aspect('equal')
ax.axis('off')  # 关闭坐标轴刻度和标签

# 初始化散点对象
scat = ax.scatter([], [], s=2, c='white', alpha=0.4, marker='o', edgecolors='none')

# 预计算一些常量和数据
i = np.arange(10000)  # 使用 10000 个点
x = i.astype(float)
y = i / 235.0
e = y / 8.0 - 13.0

# 动画更新函数
def update(frame):
    t = frame * np.pi / 240  # 计算当前时间 t

    # 计算 k 和 d
    k = (4 + np.sin(y * 2 - t) * 3) * np.cos(x / 29)
    d = np.sqrt(k**2 + e**2)  # 使用 np.linalg.norm([k, e], axis=0) 也可以，但 sqrt 更直接

    # 计算 q
    q = 3 * np.sin(k * 2) + 0.3 / k + np.sin(y / 25) * k * (9 + 4 * np.sin(e * 9 - d * 3 + t * 2))

    # 计算新的 X 和 Y 数据
    new_x = q + 30 * np.cos(d - t) + 200
    new_y = 620 - q * np.sin(d - t) - d * 39

    # 计算动态颜色
    colors = np.array([[0.5 + 0.5 * np.sin(x_i/50 + t), 
                       0.3 + 0.6 * np.cos(y_i/40 - t * 1.2), 
                       0.7 + 0.3 * np.sin((x_i + y_i)/60 + t * 0.8)] for x_i, y_i in zip(new_x, new_y)])
    # 确保颜色值在0-1范围内
    colors = np.clip(colors, 0, 1)
    scat.set_facecolors(colors)

    # 更新散点的数据
    scat.set_offsets(np.column_stack((new_x, new_y)))

    return scat,

# 创建动画
# interval: 每帧之间的间隔（毫秒），值越小动画越快
# blit: 优化绘制，只重绘变化的部分（可能在某些后端不工作）
ani = FuncAnimation(fig, update, interval=20, blit=False, cache_frame_data=False) # blit=False 更兼容

# 显示图形窗口
plt.tight_layout()
plt.show()

# 注意：在某些环境中，plt.show() 会阻塞程序，动画会在此处运行
# 在交互式环境（如 Jupyter Notebook）中，可能需要特殊的后端支持




