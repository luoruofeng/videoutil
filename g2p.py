import os
from pydub import AudioSegment
import subprocess

def convert_mp3_to_wav(mp3_file):
    wav_file = os.path.splitext(mp3_file)[0] + '.wav'
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')
    return wav_file

def run_mfa(wav_file, text_file, output_dir, g2p_model):
    # Command to run MFA
    command = [
        "mfa_align",
        wav_file,
        text_file,
        g2p_model,
        output_dir
    ]
    subprocess.run(command)

def process_directory(directory, g2p_model):
    for file in os.listdir(directory):
        if file.lower().endswith('.mp3'):
            mp3_file = os.path.join(directory, file)
            wav_file = convert_mp3_to_wav(mp3_file)
            
            text_file = os.path.splitext(wav_file)[0] + '.txt'
            output_dir = os.path.join(directory, 'alignment_output')
            os.makedirs(output_dir, exist_ok=True)
            
            if os.path.exists(text_file):
                print(f"Running MFA on {wav_file} with {text_file}...")
                run_mfa(wav_file, text_file, output_dir, g2p_model)
            else:
                print(f"Lyrics file {text_file} not found for {wav_file}. Skipping...")

if __name__ == "__main__":
    current_directory = os.getcwd()
    g2p_model = "path_to_your_g2p_model"  # Replace with the path to your G2P model
    process_directory(current_directory, g2p_model)
