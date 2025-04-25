import subprocess
import os

def create_glowing_text_video(text, font_path, output_path, duration=5, resolution="1280x720", font_size=60, text_color="white@0.5", glow_color="yellow@1", blur_radius=5):
    """Creates a video with glowing text.

    Args:
        text: The text to display.
        font_path: Path to the font file.
        output_path: Path to save the output video.
        duration: Duration of the video in seconds.
        resolution: Resolution of the video (e.g., "1280x720").
        font_size: Size of the font.
        text_color: Color of the text (e.g., "white@0.5" for white with 50% opacity).
        glow_color: Color of the glow (e.g., "yellow@1" for fully opaque yellow).
        blur_radius: Radius of the blur effect.
    """

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    width, height = resolution.split("x")

    try:
        width = int(width)
        height = int(height)
    except ValueError:
        raise ValueError("Invalid resolution format. Use 'WIDTHxHEIGHT' (e.g., '1280x720').")
    
    command = [
        "ffmpeg",
        "-f", "lavdevice",
        "-i", f"color=c=black:s={resolution}:d={duration}",
        "-vf",
        f"drawtext=text='{text}':fontfile={font_path}:x=(w-tw)/2:y=(h-th)/2:fontsize={font_size}:fontcolor={text_color}:shadowcolor={glow_color}:shadowx=0:shadowy=0,boxblur=luma_radius={blur_radius},overlay=x=(W-w)/2:y=(H-h)/2",
        "-c:v", "libx264", "-crf", "18", output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video created successfully: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating video: {e}")
        print(f"FFmpeg command used: {' '.join(command)}") # Print the full command for debugging
    except FileNotFoundError:
        print("FFmpeg not found. Make sure it's installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example Usage:
text_to_display = "नमस्ते, आप कैसे हैं"
font_file = "Tillana-Bold.ttf"  # Replace with the actual path to your font
output_video_file = "output_glowing_text.mp4"

try:
    create_glowing_text_video(text_to_display, font_file, output_video_file)
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)

# Example with different parameters:
text2 = "Another Example"
output2 = "output_glowing_text2.mp4"
try:
    create_glowing_text_video(text2, font_file, output2, duration=3, font_size=48, glow_color="blue@0.7", blur_radius=3)
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)