import os
import whisper
from pydub import AudioSegment

# 加载 Whisper 模型
model = whisper.load_model("large")

# 定义一个函数来提取音素时长
def extract_phoneme_durations(text, segments):
    phoneme_durations = []
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        duration = end_time - start_time

        # 将每个汉字的音素时长放入列表
        for char in segment['text']:
            phoneme_duration = round(duration / len(segment['text']), 4)
            phoneme_durations.append(phoneme_duration)
    
    return phoneme_durations

# 定义遍历并处理文件的函数
def process_mp3_files():
    for filename in os.listdir("."):
        if filename.endswith(".mp3"):
            audio = AudioSegment.from_mp3(filename)
            audio.export("temp.wav", format="wav")

            # 使用 Whisper 进行语音识别
            result = model.transcribe("temp.wav", language="zh")

            # 提取汉字音素时长
            phoneme_durations = extract_phoneme_durations(result['text'], result['segments'])

            # 打印格式化结果
            formatted_output = " | ".join([" ".join(map(str, phoneme_durations[i:i+len(result['segments'][i]['text'])]))
                                            for i in range(len(result['segments']))])
            print(formatted_output)

# 执行文件处理函数
process_mp3_files()
