import torch
from transformers import M4SingerModel, M4SingerTokenizer

# 加载模型和分词器
model_name = "m4singer-large"  # 请替换为实际模型名称
model = M4SingerModel.from_pretrained(model_name)
tokenizer = M4SingerTokenizer.from_pretrained(model_name)

# 定义歌词、时长和音符
lyrics = "风儿轻轻吹，花儿慢慢开"  # 示例歌词
durations = [0.5, 0.5, 1.0, 0.5, 0.5, 1.0]  # 每个字的时长（单位：秒）
notes = [60, 62, 64, 65, 67, 69]  # 每个字对应的MIDI音符数字

# 确保输入的歌词、时长、音符的数量一致
assert len(lyrics) == len(durations) == len(notes), "歌词、时长和音符的长度必须相等"

# 对输入进行编码
inputs = tokenizer(lyrics, return_tensors="pt", add_special_tokens=False)

# 将时长和音符作为额外输入
inputs['durations'] = torch.tensor(durations).unsqueeze(0)  # 增加batch维度
inputs['notes'] = torch.tensor(notes).unsqueeze(0)  # 增加batch维度

# 生成新的音乐
with torch.no_grad():
    outputs = model(**inputs)

# 假设输出包含生成的音频特征
generated_audio = outputs.audio_features

# 保存生成的音频到文件 (可使用其他库如 librosa 或 pydub)
# 这里假设我们已经得到了音频特征，可以使用其他工具将其保存为wav或mp3文件
import numpy as np
import soundfile as sf

# 假设生成的音频特征是一个numpy数组
# 将其转换为wav文件并保存
sf.write('generated_music.wav', np.array(generated_audio), samplerate=16000)
