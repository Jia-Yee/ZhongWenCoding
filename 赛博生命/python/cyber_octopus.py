#!/usr/bin/env python3
"""
彩色章鱼视频生成器

基于现有的彩色章鱼动画代码，添加了视频保存功能
可以生成mp4格式的视频文件

用法:
    python3 cyber_octopus.py

参数配置:
    - fps: 视频帧率，默认20
    - bitrate: 视频比特率，默认1800
    - codec: 视频编码器，默认libx264
    - output_file: 输出视频文件名，默认cyber_octopus.mp4
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

OUTPUT_FILE = 'cyber_octopus.mp4'  # 输出视频文件名
FRAME_COUNT = 360  # 视频帧数（约18秒），确保章鱼完成完整运动周期
DPI = 100  # 视频分辨率（每英寸像素数）
VIDEO_WIDTH = 1280  # 视频宽度（像素）
VIDEO_HEIGHT = 720  # 视频高度（像素）

# 预计算一些常量和数据
n_points = 15000  # 点的数量
i = np.arange(n_points)
x = i.astype(float)
y = i / 40.0

# 章鱼的触手数量
tentacle_count = 8


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
    
    # 计算章鱼头部位置，使其能游出屏幕上方，从下方回来
    # 使用正弦函数实现上下移动
    head_x = 250 + 5 * np.sin(t * 0.5)
    # 计算垂直位置，使章鱼能游出屏幕
    head_y = 250 + 400 * np.sin(t * 0.5)  # 振幅400，频率0.5
    head_radius = 60
    
    # 处理屏幕边界，使章鱼从下方返回
    if head_y > 700:  # 超出屏幕上方
        head_y = -200  # 从下方重新进入
    
    # 计算每个点的位置
    new_x = []
    new_y = []
    
    for i in range(n_points):
        # 计算点属于哪个触手
        tentacle_index = i % tentacle_count
        # 计算点在触手上的位置（0-1）
        tentacle_position = (i // tentacle_count) / (n_points // tentacle_count)
        
        # 计算触手角度，添加一些随机变化使触手更加自然
        angle = (tentacle_index / tentacle_count) * 2 * np.pi - np.pi/2 + 0.1 * np.sin(t * 0.5 + tentacle_index)
        
        # 计算点的位置
        if tentacle_position < 0.2:  # 头部区域
            # 改进头部形状，使其更加圆润和有机
            r = head_radius * tentacle_position * 5 * (1 + 0.1 * np.sin(t * 0.3 + tentacle_index))
            # 头部的轻微变形
            r *= (1 + 0.05 * np.cos(angle * 2 + t * 0.2))
            x = head_x + r * np.cos(angle)
            y = head_y + r * np.sin(angle)
        else:  # 触手区域
            # 触手的基础位置，优化与头部的连接
            base_radius = head_radius * (1 + 0.1 * np.sin(t * 0.3 + tentacle_index))
            base_x = head_x + base_radius * np.cos(angle)
            base_y = head_y + base_radius * np.sin(angle)
            
            # 参考赛博蠕虫的数学公式，为触手添加类似蠕虫尾巴的波浪效果
            # 调整参数以适应触手的长度和角度
            tentacle_length = 150 * (tentacle_position - 0.2) / 0.8  # 调整长度范围
            
            # 应用赛博蠕虫的公式
            y_worm = tentacle_length / 235.0
            e = y_worm / 8.0 - 13.0
            k = (4 + np.sin(y_worm * 2 - t - tentacle_index) * 3) * np.cos(tentacle_length / 29)
            d = np.sqrt(k**2 + e**2)
            q = 3 * np.sin(k * 2) + 0.3 / k + np.sin(y_worm / 25) * k * (9 + 4 * np.sin(e * 9 - d * 3 + t * 2 + tentacle_index))
            
            # 计算触手的波动
            wave_x = q * np.cos(angle) + 30 * np.cos(d - t - tentacle_index) * np.sin(angle + np.pi/2)
            wave_y = q * np.sin(angle) - 30 * np.sin(d - t - tentacle_index) * np.cos(angle + np.pi/2)
            
            # 增加触手的粗细变化，使连接更加自然
            thickness = 1.0 - 0.8 * (tentacle_position - 0.2) / 0.8
            # 优化触手根部的粗细过渡
            thickness *= (1 + 0.5 * (1 - (tentacle_position - 0.2) / 0.8))
            
            # 计算点的最终位置
            x = base_x + tentacle_length * np.cos(angle) + wave_x * thickness
            y = base_y + tentacle_length * np.sin(angle) + wave_y * thickness
        
        new_x.append(x)
        new_y.append(y)
    
    # 动态调整颜色，使用彩色效果
    colors = np.array([[0.2 + 0.3 * np.sin(pt_y/20 + t), 
                       0.4 + 0.4 * np.cos(pt_x/40 - t * 1.2), 
                       0.6 + 0.3 * np.sin((pt_x + pt_y)/30 + t * 0.8)] for pt_x, pt_y in zip(new_x, new_y)])
    # 确保颜色值在0-1范围内
    colors = np.clip(colors, 0, 1)
    scat.set_facecolors(colors)
    
    # 更新散点的数据
    scat.set_offsets(np.column_stack((new_x, new_y)))
    
    return scat,


def generate_video():
    """生成彩色章鱼视频"""
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
