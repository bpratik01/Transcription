import subprocess
import logging
import os

def convert_video_to_audio(video_file, audio_file):
    logger = logging.getLogger(__name__)
    try:
        # Check if input video file exists
        if not os.path.exists(video_file):
            raise FileNotFoundError(f"Input video file not found: {video_file}")

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(audio_file), exist_ok=True)

        # Construct ffmpeg command
        command = [
            "ffmpeg",
            "-i", video_file,
            "-vn",  # Disable video
            "-acodec", "libmp3lame",
            "-ab", "128k",
            "-ar", "44100",
            "-y",  # Overwrite output file if it exists
            audio_file
        ]

        # Run ffmpeg command
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        logger.info(f"Successfully converted {video_file} to {audio_file}")
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error converting {video_file}: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error converting {video_file}: {str(e)}")
        raise