import os
import logging
from datetime import datetime

def setup_logging(level, log_dir, log_file):
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Generate a timestamp for each run and create a unique log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"{timestamp}_{log_file}")

    # Set up logging to file and console
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def get_video_files(directory):
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(video_extensions)]

def ensure_directories_exist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
