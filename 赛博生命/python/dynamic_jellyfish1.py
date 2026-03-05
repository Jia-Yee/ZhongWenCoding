#!/usr/bin/env python3
"""
彩色水母视频生成器

基于现有的彩色水母动画代码，添加了视频保存功能
可以生成mp4格式的视频文件

用法:
    python dynamic_jellyfish1.py

参数配置:
    - fps: 视频帧率，默认20
    - bitrate: 视频比特率，默认1800
    - codec: 视频编码器，默认libx264
    - output_file: 输出视频文件名，默认cyber_jellyfish.mp4
    - frame_count: 视频帧数，默认200（约10秒）
    - dpi: 视频分辨率（每英寸像素数），默认100
    - video_width: 视频宽度（像素），默认1920
    - video_height: 视频高度（像素），默认1080

使用示例:
    # 生成1920x1080的全高清视频
    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    
    # 生成1280x720的高清视频
    VIDEO_WIDTH = 1280
    VIDEO_HEIGHT = 720
    
    # 生成800x600的标清视频
    VIDEO_WIDTH = 800
    VIDEO_HEIGHT = 600

视频尺寸计算:
    视频的实际像素尺寸由VIDEO_WIDTH和VIDEO_HEIGHT参数直接决定
    figsize（英寸） = (VIDEO_WIDTH/DPI, VIDEO_HEIGHT/DPI)
    例如：1920x1080像素，100 DPI → figsize=(19.2, 10.8)英寸
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter

# 视频参数配置
VIDEO_PARAMS = {
    'fps': 20,  # 帧率
    'bitrate': 1800,  # 比特率
    'codec': 'libx264'  # 编码器
}

OUTPUT_FILE = 'cyber_jellyfish.mp4'  # 输出视频文件名
FRAME_COUNT = 360  # 视频帧数（约18秒），确保水母回到起始位置
DPI = 100  # 视频分辨率（每英寸像素数）
VIDEO_WIDTH = 1280  # 视频宽度（像素）
VIDEO_HEIGHT = 720  # 视频高度（像素）


def init_animation():
    """初始化动画环境"""
    # 根据视频宽度和高度计算figsize（英寸）
    fig_width = VIDEO_WIDTH / DPI
    fig_height = VIDEO_HEIGHT / DPI
    
    # 设置图形和坐标轴
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='black')
    ax.set_facecolor('black')
    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.set_aspect('equal')
    ax.axis('off')  # 关闭坐标轴刻度和标签

    # 初始化散点对象
    scat = ax.scatter([], [], s=1, c='white', alpha=0.4, marker='o', edgecolors='none')

    return fig, ax, scat


def precompute_data():
    """预计算常量和数据"""
    i = np.arange(10000)  # 使用 10000 个点
    x = np.mod(i, 200)
    y = i / 43.0
    k = 5 * np.cos(x / 14.0) * np.cos(y / 30.0)
    e = y / 8.0 - 13.0
    d = (k**2 + e**2) / 59.0 + 4.0
    a = np.arctan2(k, e)  # 使用 np.arctan2 替代 atan2
    
    return x, y, k, e, d, a


def update(frame, scat, x, y, k, e, d, a):
    """动画更新函数
    
    Args:
        frame: 当前帧序号
        scat: 散点对象
        x, y, k, e, d, a: 预计算的数据
    """
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


def generate_video():
    """生成彩色水母视频"""
    print(f"初始化动画环境...")
    fig, ax, scat = init_animation()
    
    print(f"预计算数据...")
    x, y, k, e, d, a = precompute_data()
    
    print(f"创建动画对象...")
    # 创建动画
    # interval: 每帧之间的间隔（毫秒），值越小动画越快
    # blit: 优化绘制，只重绘变化的部分（可能在某些后端不工作）
    ani = FuncAnimation(fig, update, fargs=(scat, x, y, k, e, d, a), 
                       interval=50, blit=False, cache_frame_data=False) 
    
    print(f"正在生成视频: {OUTPUT_FILE}")
    print(f"视频尺寸: {VIDEO_WIDTH}x{VIDEO_HEIGHT} 像素")
    print(f"视频分辨率: {DPI} DPI")
    print(f"视频时长: {FRAME_COUNT/VIDEO_PARAMS['fps']:.1f} 秒")
    
    # 创建FFMpegWriter实例
    writer = FFMpegWriter(**VIDEO_PARAMS)
    
    # 保存视频
    with writer.saving(fig, OUTPUT_FILE, dpi=DPI):
        for i in range(FRAME_COUNT):  # 生成指定帧数的视频
            ani._draw_frame(i)
            writer.grab_frame()
            if i % 20 == 0:
                print(f"已完成 {i}/{FRAME_COUNT} 帧")
    
    print(f"视频生成完成: {OUTPUT_FILE}")
    print(f"视频保存在: {OUTPUT_FILE}")
    print(f"视频尺寸: {VIDEO_WIDTH}x{VIDEO_HEIGHT} 像素")


if __name__ == "__main__":
    generate_video()

# 注意：在某些环境中，plt.show() 会阻塞程序，动画会在此处运行
# 在交互式环境（如 Jupyter Notebook）中，可能需要特殊的后端支持




