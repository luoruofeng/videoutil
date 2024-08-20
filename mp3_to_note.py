import os
import librosa
import numpy as np

def extract_notes_from_audio(y, sr):
    # Onset detection to segment the audio into syllables
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # Extract pitches
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)
    
    # Convert pitches to notes
    note_sequence = []
    for onset in onset_frames:
        pitch_slice = pitches[:, onset]
        index = np.argmax(pitch_slice)
        pitch = pitch_slice[index]
        
        if pitch == 0:  # Treat as a rest
            note_sequence.append('rest')
        else:
            note = librosa.hz_to_midi(pitch)
            note_name = librosa.midi_to_note(note)
            note_sequence.append(note_name)
    
    return note_sequence

def format_notes(note_sequence):
    formatted_output = ' | '.join(note_sequence)
    return formatted_output

def process_mp3_file(filepath):
    y, sr = librosa.load(filepath, sr=None)
    note_sequence = extract_notes_from_audio(y, sr)
    formatted_notes = format_notes(note_sequence)
    return formatted_notes

def process_all_mp3_files(directory):
    output_file = os.path.join(directory, 'sheet_music_output.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for filename in os.listdir(directory):
            if filename.endswith(".mp3"):
                filepath = os.path.join(directory, filename)
                print(f"Processing {filename}...")
                formatted_notes = process_mp3_file(filepath)
                f.write(f"Sheet music for {filename}:\n{formatted_notes}\n\n")
                print(f"Sheet music for {filename}:\n{formatted_notes}\n")
    
    print(f"All sheet music has been saved to {output_file}")

# Specify the directory containing the MP3 files
directory = './'  # Current directory
process_all_mp3_files(directory)
