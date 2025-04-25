import subprocess
from blank_trimmer import process_audio
import os

def add_echo_effect(input_file: str, output_file: str):
    """
    Adds an echo effect to an audio file using ffmpeg.

    Parameters:
        input_file (str): The path to the input audio file.
        output_file (str): The path to save the output audio file.
    """
    try:
        # Construct the ffmpeg command
        command = [
            "ffmpeg",
            "-i", input_file,
            "-af", "aecho=1:0.35:80:0.15",
            output_file
        ]
        # Run the command
        subprocess.run(command, check=True)
        print(f"Echo effect applied successfully. Output saved to {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error applying echo effect: {e}")
    except FileNotFoundError:
        print("ffmpeg not found. Please ensure it is installed and in your PATH.")




def find_file_with_max_difference(folder_path):
    # Dictionary to store file names and their differences
    file_differences = {}

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".mp3"):
            try:
                # Remove the .mp3 extension and the trailing 's'
                base_name = os.path.splitext(file_name)[0].rstrip('s')
                
                # Extract the numerical range from the file name
                start, end = map(float, base_name.split("-"))

                # Calculate the difference
                difference = abs(end - start)

                # Store the file name and difference
                file_differences[file_name] = difference

            except ValueError:
                print(f"Skipping file with invalid format: {file_name}")

    # Find the file with the maximum difference
    if file_differences:
        max_difference_file = max(file_differences, key=file_differences.get)
        #print(f"File with the highest difference: {max_difference_file} ({file_differences[max_difference_file]:.2f}s)")
        max_diff=f"File with the highest difference: {max_difference_file}"
        return max_diff

    else:
        return "No valid .mp3 files found in the folder."

#Add echo to voices 
add_echo_effect("vocal/female.mp3", "vocal/edited_female.mp3")
add_echo_effect("vocal/male.mp3", "vocal/edited_male.mp3")

##Trim Blank voices in male voice
input_audio = "vocal/edited_male.mp3"  # Replace with your .mp3 audio file path
output_dir = "output_segments"  # Directory to save the cut segments
process_audio(input_audio, output_dir)

##Get the highest male audio segment
folder_path = "output_segments"  # Replace with your folder path
print(find_file_with_max_difference(folder_path))


