import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 初始化全局时间变量
t = 0.0

def mag(k, e):
    """计算向量模长"""
    return np.sqrt(k**2 + e**2)

def calculate_points(t_val):
    """向量化计算所有点的坐标"""
    # 生成i的向量化数组（10000到1的倒序）
    i = np.arange(10000, 0, -1, dtype=np.float64)
    
    # 计算基础参数
    x = i % 200
    y = i / 43.0
    
    # 计算k和e分量
    k = 5.0 * np.cos(x / 14.0) * np.cos(y / 30.0)
    e = y / 8.0 - 13.0
    
    # 计算d
    d = (k**2 + e**2) / 59.0 + 4.0  # 等价于mag(k,e)**2/59 +4
    
    # 计算q（核心公式）
    atan = np.arctan2(e, k)  # atan2(k,e)对应数学上的arctan(e/k)
    q = 60.0 - 3.0 * np.sin(atan * e) + k * (3.0 + (4.0 / d) * np.sin(d**2 - 2 * t_val))
    
    # 计算c（中间变量）
    c = d / 2.0 + e / 99.0 - t_val / 18.0
    
    # 计算最终坐标
    px = q * np.sin(c) + 200.0
    py = (q + 9.0 * d) * np.cos(c) + 200.0
    
    return px, py

def update(frame):
    global t
    # 时间递增（PI/20）
    t += np.pi / 20
    
    ax.clear()
    # 设置绘图参数（黑色背景，400x400范围）
    ax.set_facecolor((0, 0, 0))
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.set_aspect('equal')
    ax.invert_yaxis()  
    
    # 计算并绘制点（白色，透明度约0.66）
    px, py = calculate_points(t)
    ax.scatter(px, py, s=1, c='white', alpha=0.66, edgecolors='none')

# 初始化图形
fig, ax = plt.subplots(figsize=(4, 4))
fig.patch.set_facecolor((0, 0, 0))  # 窗口背景黑色
ax.set_facecolor((0, 0, 0))         # 坐标轴背景黑色

# 创建动画（约60帧/秒）
ani = animation.FuncAnimation(
    fig, update,
    interval=16,  # 16ms间隔≈60fps
    blit=False,
    frames=300
)

# 保存为GIF
ani.save(
    '1.gif',
    writer='pillow',
    fps=45,                   # 帧率（决定每秒钟显示多少帧）
    dpi=72
)

plt.show()

