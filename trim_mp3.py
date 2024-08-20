import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

# 定义裁剪函数
def trim_silence(mp3_file):
    # 加载MP3文件
    audio = AudioSegment.from_mp3(mp3_file)
    
    # 检测非静音段
    non_silence_ranges = detect_nonsilent(audio, min_silence_len=1000, silence_thresh=-50)
    
    if non_silence_ranges:
        start_trim = non_silence_ranges[0][0]
        end_trim = non_silence_ranges[-1][1]
        
        # 裁剪音频
        trimmed_audio = audio[start_trim:end_trim]
        
        # 覆盖保存裁剪后的音频
        trimmed_audio.export(mp3_file, format="mp3")
        print(f"裁剪完成: {mp3_file}")
    else:
        print(f"没有检测到可裁剪的静音段: {mp3_file}")

# 获取当前文件夹下所有MP3文件
mp3_files = [f for f in os.listdir() if f.endswith(".mp3")]

# 裁剪每个MP3文件的静音部分并保存
for mp3_file in mp3_files:
    print(f"开始裁剪: {mp3_file}")
    trim_silence(mp3_file)
