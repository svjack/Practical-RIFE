git clone https://github.com/hzwer/Practical-RIFE

python inference_video.py --multi=2 --video=优菈相亲视频.mp4

import os
from moviepy.editor import VideoFileClip
from PIL import Image

def save_video_frames(video_path, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 加载视频文件
    video_clip = VideoFileClip(video_path)

    # 逐帧读取并保存
    for i, frame in enumerate(video_clip.iter_frames()):
        # 生成文件名
        frame_filename = os.path.join(output_folder, f"frame_{i:04d}.png")

        # 将 NumPy 数组转换为 PIL 图像并保存
        img = Image.fromarray(frame)
        img.save(frame_filename)

    print(f"所有帧已保存到 {output_folder}")

# 示例用法
video_path = "../刻晴摇_short.mp4"  # 你的视频文件路径
output_folder = "刻晴摇_short_pic_dir"    # 保存帧的文件夹名称
save_video_frames(video_path, output_folder)

#### take some pics from 刻晴摇_short_pic_dir to 刻晴摇_inter_pic_dir

import os
from moviepy.editor import ImageSequenceClip

def create_video_from_images(image_folder, output_video_path, video_length):
    # 获取文件夹中的所有图片文件
    image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))])

    # 计算帧率
    num_frames = len(image_files)
    fps = num_frames / video_length

    # 创建视频
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_video_path, codec='libx264')

    print(f"视频已保存到 {output_video_path}")

# 示例用法
image_folder = "刻晴摇_inter_pic_dir"  # 包含图片的文件夹路径
output_video_path = "刻晴摇_inter_video.mp4"  # 输出视频的路径
video_length = 3  # 视频长度（秒）
create_video_from_images(image_folder, output_video_path, video_length)

python inference_video.py --multi=128 --video=刻晴摇_inter_video.mp4

import os
from moviepy.editor import VideoFileClip, CompositeVideoClip

def merge_videos_horizontally(video_path1, video_path2, output_video_path):
    # 加载两个视频文件
    clip1 = VideoFileClip(video_path1)
    clip2 = VideoFileClip(video_path2)

    # 使用两个视频中较长的时长作为最终视频的时长
    max_duration = max(clip1.duration, clip2.duration)

    # 如果某个视频的时长较短，则将其循环播放以匹配较长的时长
    if clip1.duration < max_duration:
        clip1 = clip1.loop(duration=max_duration)
    if clip2.duration < max_duration:
        clip2 = clip2.loop(duration=max_duration)

    # 计算合成视频的宽度和高度
    total_width = clip1.w + clip2.w
    total_height = max(clip1.h, clip2.h)

    # 创建一个合成视频剪辑，将两个视频横向合并
    final_clip = CompositeVideoClip([
        clip1.set_position(("left", "center")),
        clip2.set_position(("right", "center"))
    ], size=(total_width, total_height))

    # 保存合并后的视频
    final_clip.write_videofile(output_video_path, codec='libx264')

    print(f"合并后的视频已保存到 {output_video_path}")

# 示例用法
video_path1 = "刻晴摇_inter_video.mp4"  # 第一个视频文件路径
video_path2 = "刻晴摇_inter_video_128X_298fps.mp4"  # 第二个视频文件路径
output_video_path = "刻晴摇_inter_video_compare.mp4"  # 输出视频的路径
merge_videos_horizontally(video_path1, video_path2, output_video_path)

from IPython import display
display.Video("刻晴摇_inter_video_compare.mp4")
