import os
import subprocess

def extract_audio_from_mp4(input_file, output_file):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-q:a', '0',  # Preserve audio quality
        '-map', 'a',  # Extract audio streams
        output_file
    ]
    subprocess.run(command, check=True)

def process_directory(directory):
    for file in os.listdir(directory):
        if file.lower().endswith('.mp4'):
            input_file = os.path.join(directory, file)
            output_file = os.path.join(directory, f"{os.path.splitext(file)[0]}.mp3")
            try:
                extract_audio_from_mp4(input_file, output_file)
                print(f"Extracted audio from {input_file} to {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to extract audio from {input_file}: {e}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directory(current_directory)
