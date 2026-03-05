#!/usr/bin/env python3
"""
彩色蠕虫视频生成器

基于现有的彩色蠕虫动画代码，添加了视频保存功能
可以生成mp4格式的视频文件

用法:
    python3 cyber_worm2.py

参数配置:
    - fps: 视频帧率，默认20
    - bitrate: 视频比特率，默认1800
    - codec: 视频编码器，默认libx264
    - output_file: 输出视频文件名，默认cyber_worm.mp4
    - frame_count: 视频帧数，默认360（约18秒）
    - dpi: 视频分辨率（每英寸像素数），默认100
    - video_width: 视频宽度（像素），默认1280
    - video_height: 视频高度（像素），默认720
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib.patches as patches

# 视频参数配置
VIDEO_PARAMS = {
    'fps': 20,  # 帧率
    'bitrate': 1800,  # 比特率
    'codec': 'libx264'  # 编码器
}

OUTPUT_FILE = 'cyber_worm.mp4'  # 输出视频文件名
FRAME_COUNT = 360  # 视频帧数（约18秒），确保蠕虫完成完整运动周期
DPI = 100  # 视频分辨率（每英寸像素数）
VIDEO_WIDTH = 1280  # 视频宽度（像素）
VIDEO_HEIGHT = 720  # 视频高度（像素）

# 预计算一些常量和数据
i = np.arange(10000)  # 使用 10000 个点
x = i.astype(float)
y = i / 235.0
e = y / 8.0 - 13.0


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
    scat = ax.scatter([], [], s=2, c='white', alpha=0.4, marker='o', edgecolors='none')

    return fig, ax, scat


def update(frame, scat):
    """动画更新函数
    
    Args:
        frame: 当前帧序号
        scat: 散点对象
    """
    t = frame * np.pi / 240  # 计算当前时间 t

    # 计算 k 和 d
    k = (4 + np.sin(y * 2 - t) * 3) * np.cos(x / 29)
    d = np.sqrt(k**2 + e**2)  # 使用 np.linalg.norm([k, e], axis=0) 也可以，但 sqrt 更直接

    # 计算 q
    q = 3 * np.sin(k * 2) + 0.3 / k + np.sin(y / 25) * k * (9 + 4 * np.sin(e * 9 - d * 3 + t * 2))

    # 计算新的 X 和 Y 数据，添加垂直移动使蠕虫能游出屏幕
    new_x = q + 30 * np.cos(d - t) + 200
    # 计算垂直位置，使蠕虫能游出屏幕
    vertical_offset = 300 * np.sin(t * 0.8)  # 振幅300，频率0.8
    new_y = 620 - q * np.sin(d - t) - d * 39 + vertical_offset

    # 处理屏幕边界，使蠕虫从下方返回
    for i in range(len(new_y)):
        if new_y[i] > 600:  # 超出屏幕上方
            new_y[i] = -200  # 从下方重新进入

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


def generate_video():
    """生成彩色蠕虫视频"""
    print(f"初始化动画环境...")
    fig, ax, scat = init_animation()
    
    print(f"创建动画对象...")
    # 创建动画
    ani = FuncAnimation(fig, update, fargs=(scat,), 
                       interval=20, blit=False, cache_frame_data=False)
    
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




