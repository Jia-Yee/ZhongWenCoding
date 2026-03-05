#!/usr/bin/env python3
"""
彩色蝴蝶视频生成器

基于现有的彩色蝴蝶动画代码，添加了视频保存功能
可以生成mp4格式的视频文件

用法:
    python3 cyber_butterfly.py

参数配置:
    - fps: 视频帧率，默认20
    - bitrate: 视频比特率，默认1800
    - codec: 视频编码器，默认libx264
    - output_file: 输出视频文件名，默认cyber_butterfly.mp4
    - frame_count: 视频帧数，默认360（约18秒）
    - dpi: 视频分辨率（每英寸像素数），默认100
    - video_width: 视频宽度（像素），默认1280
    - video_height: 视频高度（像素），默认720
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

OUTPUT_FILE = 'cyber_butterfly.mp4'  # 输出视频文件名
FRAME_COUNT = 360  # 视频帧数（约18秒），确保蝴蝶完成完整运动周期
DPI = 100  # 视频分辨率（每英寸像素数）
VIDEO_WIDTH = 1280  # 视频宽度（像素）
VIDEO_HEIGHT = 720  # 视频高度（像素）

# 蝴蝶的翅膀参数
wing_size = 120
body_length = 40
n_points = 15000  # 点的数量


def init_animation():
    """初始化动画环境"""
    # 根据视频宽度和高度计算figsize（英寸）
    fig_width = VIDEO_WIDTH / DPI
    fig_height = VIDEO_HEIGHT / DPI
    
    # 设置图形和坐标轴
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor='black')
    ax.set_facecolor('black')
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    ax.set_aspect('equal')
    ax.axis('off')  # 关闭坐标轴刻度和标签

    # 初始化散点对象
    scat = ax.scatter([], [], s=2, c='cyan', alpha=0.6, marker='o', edgecolors='none')

    return fig, ax, scat


def update(frame, scat):
    """动画更新函数
    
    Args:
        frame: 当前帧序号
        scat: 散点对象
    """
    t = frame * np.pi / 180  # 计算当前时间 t
    
    # 计算蝴蝶身体位置，使其能游出屏幕上方，从下方回来
    # 使用正弦函数实现上下移动
    body_x = 250
    # 计算垂直位置，使蝴蝶能游出屏幕
    body_y = 250 + 400 * np.sin(t * 0.5)  # 振幅400，频率0.5
    
    # 处理屏幕边界，使蝴蝶从下方返回
    if body_y > 700:  # 超出屏幕上方
        body_y = -200  # 从下方重新进入
    
    # 计算每个点的位置
    new_x = []
    new_y = []
    
    for i in range(n_points):
        # 计算点属于左翅膀还是右翅膀
        is_left_wing = i % 2 == 0
        # 计算点在翅膀上的位置（0-1）
        wing_position = (i // 2) / (n_points // 2)
        
        if wing_position < 0.1:  # 身体区域
            # 改进身体形状，使其更加细长
            y = body_y + (wing_position * 10 - 0.5) * body_length
            # 身体的粗细变化
            body_thickness = 1.0 - 0.6 * abs(wing_position * 10 - 0.5)
            x = body_x + 5 * body_thickness * np.sin(t * 2)  # 身体轻微摆动
        else:  # 翅膀区域
            # 调整位置范围到0-1
            wing_pos = (wing_position - 0.1) / 0.9
            
            # 改进翅膀的角度和形状，使其更加自然
            angle = wing_pos * np.pi / 2
            # 翅膀的形状函数，使用更复杂的数学公式
            radius = wing_size * np.sin(angle) * (1 + 0.3 * np.cos(angle * 3))
            
            # 翅膀的波动，增加更多的频率和幅度
            wave = 10 * np.sin(wing_pos * 5 - t * 2) + 5 * np.sin(wing_pos * 10 - t * 3)
            # 翅膀的边缘波动
            edge_wave = 3 * np.sin(wing_pos * 20 - t * 4)
            
            # 计算左右翅膀的位置
            if is_left_wing:
                x = body_x - radius * np.cos(angle) + wave + edge_wave
                y = body_y + radius * np.sin(angle) + 2 * np.sin(t * 1.5)  # 上下浮动
            else:
                x = body_x + radius * np.cos(angle) - wave - edge_wave
                y = body_y + radius * np.sin(angle) + 2 * np.sin(t * 1.5)  # 上下浮动
        
        new_x.append(x)
        new_y.append(y)
    
    # 动态调整颜色，使用更加丰富的多彩方案
    colors = np.array([[0.8 + 0.2 * np.sin(y/15 + t * 1.5), 
                       0.4 + 0.5 * np.cos(x/30 - t * 1.8), 
                       0.6 + 0.4 * np.sin((x + y)/25 + t * 1.2)] for x, y in zip(new_x, new_y)])
    # 确保颜色值在0-1范围内
    colors = np.clip(colors, 0, 1)
    scat.set_facecolors(colors)
    
    # 更新散点的数据
    scat.set_offsets(np.column_stack((new_x, new_y)))
    
    return scat,


def generate_video():
    """生成彩色蝴蝶视频"""
    print(f"初始化动画环境...")
    fig, ax, scat = init_animation()
    
    print(f"创建动画对象...")
    # 创建动画
    ani = FuncAnimation(fig, update, fargs=(scat,), 
                       interval=15, blit=False, cache_frame_data=False)
    
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
