import os
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_mp3(file_path)
    audio.export("temp.wav", format="wav")
    
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='zh-CN')
            return text
        except sr.UnknownValueError:
            return "Audio unintelligible"
        except sr.RequestError as e:
            return f"Could not request results; {e}"

def process_directory(directory):
    for file in os.listdir(directory):
        if file.lower().endswith('.mp3'):
            input_file = os.path.join(directory, file)
            output_file = os.path.join(directory, f"{os.path.splitext(file)[0]}.txt")
            
            print(f"Processing {input_file}")
            text = transcribe_audio(input_file)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"Transcription for {input_file}:")
            print(text)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directory(current_directory)
