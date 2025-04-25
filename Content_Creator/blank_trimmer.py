from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os

def find_silence_periods(audio_path, silence_thresh=-40, min_silence_len=500):
    # Load the audio file (supports MP3)
    audio = AudioSegment.from_file(audio_path)
    
    # Detect nonsilent chunks based on silence threshold and minimum silence length
    nonsilent_chunks = detect_nonsilent(
        audio,                           # Audio segment
        min_silence_len=min_silence_len, # Minimum silence length in milliseconds
        silence_thresh=silence_thresh    # Silence threshold in dBFS (default is -40 dBFS)
    )
    
    return nonsilent_chunks

def save_segments(audio_path, nonsilent_chunks, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load the original audio
    audio = AudioSegment.from_file(audio_path)
    
    # Save each nonsilent chunk with a name reflecting its position in the original audio
    for start, end in nonsilent_chunks:
        # Convert start and end time from milliseconds to seconds
        start_sec = start / 1000
        end_sec = end / 1000
        segment = audio[start:end]
        
        # Create filename using start and end time
        output_filename = f"{start_sec:.1f}-{end_sec:.1f}s.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        segment.export(output_path, format="mp3")
        print(f"Saved segment {start_sec:.1f}-{end_sec:.1f}s to {output_path}")

def process_audio(input_audio, output_dir, silence_thresh=-40, min_silence_len=500):
    nonsilent_chunks = find_silence_periods(input_audio, silence_thresh, min_silence_len)
    save_segments(input_audio, nonsilent_chunks, output_dir)

# Usage
#input_audio = "vocal/edited_male.mp3"  # Replace with your .mp3 audio file path
#output_dir = "output_segments"  # Directory to save the cut segments
#process_audio(input_audio, output_dir)
