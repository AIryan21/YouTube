import subprocess
import re
import os

def merge_audio_files(audio1_path, audio2_path):
    # Ensure audio paths are absolute
    audio1_path = os.path.abspath(audio1_path)
    audio2_path = os.path.abspath(audio2_path)

    # Check if the input files exist
    if not os.path.exists(audio1_path):
        print(f"Error: The first audio file {audio1_path} does not exist.")
        return

    if not os.path.exists(audio2_path):
        print(f"Error: The second audio file {audio2_path} does not exist.")
        return

    # Extract the merge position from the second audio file name
    match = re.search(r'(\d+\.\d+)-(\d+\.\d+)s', audio2_path)
    if match:
        start_time = float(match.group(1))  # Start time in seconds
        end_time = float(match.group(2))    # End time in seconds

        # Temporary file to hold the second audio clipped to the specified range
        temp_audio2_path = 'temp_audio2.mp3'

        # Clip the second audio file to the specified range using ffmpeg CLI
        clip_command = [
            'ffmpeg', '-i', audio2_path, '-ss', str(start_time), '-to', str(end_time), '-c', 'copy', temp_audio2_path
        ]
        clip_result = subprocess.run(clip_command, capture_output=True, text=True)

        if clip_result.returncode != 0:
            print(f"Error clipping the second audio: {clip_result.stderr}")
            return

        # Check if the temporary clipped audio file exists
        if not os.path.exists(temp_audio2_path):
            print(f"Error: The temporary file {temp_audio2_path} was not created.")
            return

        # Merge the first audio with the clipped second audio using ffmpeg CLI
        merged_audio_path = 'merged_output.mp3'
        merge_command = [
            'ffmpeg', '-i', audio1_path, '-i', temp_audio2_path, '-filter_complex', '[0][1]concat=n=2:v=0:a=1', merged_audio_path
        ]
        merge_result = subprocess.run(merge_command, capture_output=True, text=True)

        if merge_result.returncode != 0:
            print(f"Error merging the audios: {merge_result.stderr}")
            return

        print(f'Merged audio saved to {merged_audio_path}')
    else:
        print('The second audio filename does not have the correct format (start-end s).')



# Example usage
merge_audio_files('vocal/edited_female.mp3', 'vocal/edited_male.mp3')
