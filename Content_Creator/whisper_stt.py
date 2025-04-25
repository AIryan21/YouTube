import subprocess
import re

def split_subtitles(input_srt, output_srt):
    # Open the input SRT file
    with open(input_srt, 'r', encoding='utf-8') as f:
        subtitles = f.read()

    # Split the subtitles into individual blocks
    subtitle_blocks = subtitles.strip().split('\n\n')

    subtitle_index = 1  # Start the numbering from 1

    with open(output_srt, 'w', encoding='utf-8') as f:
        # Iterate through each subtitle block
        for block in subtitle_blocks:
            lines = block.split('\n')
            # Extract the index, timestamp, and subtitle text
            index = lines[0]
            timestamp = lines[1]
            text = ' '.join(lines[2:])

            # Check if there's a comma in the subtitle text to split it
            if ',' in text:
                # Find the position of the first comma
                comma_pos = text.find(',')
                
                # Split the text into two parts at the first comma
                part1 = text[:comma_pos + 1].strip()  # Include comma in the first part
                part2 = text[comma_pos + 1:].strip()  # Exclude the comma in the second part

                # Split the timestamp into start and end times
                start_time, end_time = timestamp.split(' --> ')
                start_time = start_time.strip()
                end_time = end_time.strip()

                # Split the times into hours, minutes, seconds, and milliseconds
                start_hour, start_min, start_sec = start_time.split(':')
                end_hour, end_min, end_sec = end_time.split(':')

                # Split seconds to extract milliseconds
                start_sec, start_ms = start_sec.split(',')
                end_sec, end_ms = end_sec.split(',')

                # Convert times to seconds for easier manipulation
                start_total_sec = int(start_hour) * 3600 + int(start_min) * 60 + int(start_sec)
                end_total_sec = int(end_hour) * 3600 + int(end_min) * 60 + int(end_sec)

                # Calculate the midpoint of the subtitle's duration
                mid_total_sec = (start_total_sec + end_total_sec) // 2

                # Convert the midpoint back to HH:MM:SS,MS format
                mid_hour = mid_total_sec // 3600
                mid_min = (mid_total_sec % 3600) // 60
                mid_sec = mid_total_sec % 60
                mid_time = f"{mid_hour:02}:{mid_min:02}:{mid_sec:02},{start_ms}"

                # Write the first part of the subtitle with the original start time and the new midpoint time
                f.write(f"{subtitle_index}\n{start_time} --> {mid_time}\n{part1}\n\n")
                subtitle_index += 1  # Increment the subtitle number

                # Write the second part of the subtitle with the new midpoint time and the original end time
                f.write(f"{subtitle_index}\n{mid_time} --> {end_time}\n{part2}\n\n")
                subtitle_index += 1  # Increment the subtitle number
            else:
                # If no comma, write the subtitle as it is
                f.write(f"{subtitle_index}\n{timestamp}\n{text}\n\n")
                subtitle_index += 1  # Increment the subtitle number



def transcribe_audio(file_path, language='hi', task='transcribe', model='small', output_format='srt'):
    command = [
        'whisper', file_path,
        '--language', language,
        '--task', task,
        '--model', model,
        '--output_format', output_format
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Transcription completed successfully. Output saved in {file_path}.{output_format}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
# Input and output file paths
input_audio='./audios/speech3.mp3'#The generated subtitle file and same for below
input_srt = 'speech3.srt'  # The generated subtitle file 
output_srt = 'subtitle.srt'  # The output subtitle file name
print('Proceeding...')
transcribe_audio(input_audio)
print('Transcript created...')
print('Splitting texts...')
# Call the function to split subtitles
split_subtitles(input_srt, output_srt)
print('Done..!')