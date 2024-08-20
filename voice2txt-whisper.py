import os
import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("large")
    result = model.transcribe(file_path, language='zh')

    # Extract the transcribed text without timestamps
    transcribed_text = result['text']
    return transcribed_text

def save_transcription(file_path, text):
    txt_file = f"{os.path.splitext(file_path)[0]}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved transcription to {txt_file}")

def process_mp3(file_path):
    text = transcribe_audio(file_path)
    print(f"Transcribed text from {file_path}:")
    print(text)
    save_transcription(file_path, text)

def process_directory(directory):
    for file in os.listdir(directory):
        if file.lower().endswith('.mp3'):
            file_path = os.path.join(directory, file)
            process_mp3(file_path)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directory(current_directory)
