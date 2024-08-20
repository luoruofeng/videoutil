import os
import whisper
from pypinyin import pinyin, Style

# 初始化 Whisper 模型
model = whisper.load_model("large")

def phoneme_decomposition(char):
    """
    将汉字转换为拼音，并进一步分解为音素。
    """
    pinyin_representation = pinyin(char, style=Style.TONE3, heteronym=False)[0][0]
    
    # 假设拼音的格式是 声母 + 韵母 + 声调
    tone = pinyin_representation[-1] if pinyin_representation[-1].isdigit() else ""
    if tone:
        pinyin_representation = pinyin_representation[:-1]  # 去掉声调数字
    
    # 简单分解拼音为音素（实际的音素分解可能更复杂）
    consonant = pinyin_representation[0] if pinyin_representation[0] in "bcdfghjklmnpqrstwxyz" else ""
    vowel = pinyin_representation[len(consonant):]
    
    phonemes = []
    if consonant:
        phonemes.append(consonant)
    if vowel:
        phonemes.append(vowel)
    if tone:
        phonemes.append(tone)

    return ' '.join(phonemes)

def process_mp3(file_path):
    # 使用 Whisper 模型进行语音识别
    result = model.transcribe(file_path, language="zh")
    
    # 打印出每个字及其音素
    for segment in result['segments']:
        text = segment['text']
        print(f"Recognized text: {text}")
        # 对每个字符进行处理
        for char in text:
            if char.strip():  # 过滤掉空白字符
                phoneme_str = phoneme_decomposition(char)
                print(f"| {phoneme_str} |")

def main():
    # 遍历当前目录下的所有 MP3 文件
    for file_name in os.listdir("."):
        if file_name.endswith(".mp3"):
            process_mp3(file_name)

if __name__ == "__main__":
    main()
