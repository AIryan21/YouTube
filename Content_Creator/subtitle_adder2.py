import subprocess
import re

def parse_srt(srt_file):
    """Parses the SRT file and returns a list of (start_time, end_time, text) tuples."""
    subtitles = []
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split the content by subtitle blocks (each block contains index, time, and text)
    blocks = content.strip().split("\n\n")
    
    for block in blocks:
        lines = block.splitlines()
        if len(lines) >= 3:
            time_line = lines[1]
            text = " ".join(lines[2:])
            
            # Extract start and end time from the timestamp line
            times = time_line.split(" --> ")
            if len(times) == 2:  # Ensure there are both start and end times
                start_time = times[0].strip()
                end_time = times[1].strip()
                subtitles.append((start_time, end_time, text))
            else:
                print(f"Skipping malformed subtitle block: {block}")
    
    return subtitles

def time_to_seconds(time_str):
    """Converts time from SRT format (HH:MM:SS,MS) to total seconds."""
    match = re.match(r"(\d+):(\d+):(\d+),(\d+)", time_str)
    if match:
        h, m, s, ms = match.groups()
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0
    else:
        raise ValueError(f"Invalid timestamp format: {time_str}")

def generate_ffmpeg_command(input_file, output_file, subtitles):
    """Generates the FFmpeg command to add subtitles to the video."""
    filters = []
    
    for index, (start_time, end_time, text) in enumerate(subtitles):
        # Convert time to seconds
        try:
            start_sec = time_to_seconds(start_time)
            end_sec = time_to_seconds(end_time)
        except ValueError as e:
            print(f"Skipping subtitle with error: {e}")
            continue
        
        # Calculate fade-in duration (e.g., 1 second fade-in effect)
        fade_duration = 1  # You can adjust this as needed
        
        # Alternate the font color between yellow and white
        font_color = 'yellow' if index % 2 == 0 else 'white'
        
        # Generate ffmpeg drawtext command for each subtitle with fade-in effect and direct disappearance
        filter_cmd = (f"drawtext=text='{text}':fontfile='./PragatiNarrow-Regular.ttf':fontcolor={font_color}:fontsize=60:"
                      f"x=(w-text_w)/2:y=(h-text_h)/2+90:"
                      f"alpha='if(lt(t,{start_sec}), 0, if(lt(t,{start_sec + fade_duration}), "
                      f"t-{start_sec}/{fade_duration}, if(lt(t,{end_sec}), 1, 0)))'")
        filters.append(filter_cmd)
    
    # Join all filter commands with commas
    filter_str = ",".join(filters)
    
    # Build the final ffmpeg command
    ffmpeg_cmd = f"ffmpeg -i {input_file} -vf \"{filter_str}\" {output_file}"
    return ffmpeg_cmd

def add_subtitles_to_video(input_file, srt_file, output_file):
    """Main function to add subtitles from SRT to video."""
    # Parse the subtitles from the SRT file
    subtitles = parse_srt(srt_file)
    
    if not subtitles:
        print("No valid subtitles found. Exiting.")
        return
    
    # Generate the ffmpeg command
    ffmpeg_cmd = generate_ffmpeg_command(input_file, output_file, subtitles)
    
    # Run the ffmpeg command to add subtitles
    subprocess.run(ffmpeg_cmd, shell=True)

# Example usage
input_video = "input.mp4"
output_video = "output.mp4"
srt_file = "subtitle.srt"

add_subtitles_to_video(input_video, srt_file, output_video)
