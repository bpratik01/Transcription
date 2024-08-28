import os
import yaml
import time
from concurrent.futures import ThreadPoolExecutor
from src.video_to_audio import convert_video_to_audio
from src.transcription import transcribe_audio
from src.utils import setup_logging, get_video_files, ensure_directories_exist

def main():
    # Load configuration
    with open('config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    # Ensure input, output, and log directories exist
    directories_to_create = [
        config['input_directory'],
        config['output_audio_directory'],
        config['output_transcripts_directory'],
        config['logging']['directory']
    ]
    ensure_directories_exist(directories_to_create)

    # Setup logging
    logger = setup_logging(config['logging']['level'], config['logging']['directory'], config['logging']['file'])

    # Get video files
    video_files = get_video_files(config['input_directory'])
    total_videos = len(video_files)

    logger.info(f"Found {total_videos} video files to process.")

    # Process videos in batches
    with ThreadPoolExecutor(max_workers=config['max_workers']) as executor:
        for i in range(0, total_videos, config['batch_size']):
            batch = video_files[i:i+config['batch_size']]
            futures = []

            for video_file in batch:
                audio_file = os.path.join(config['output_audio_directory'], f"{os.path.splitext(os.path.basename(video_file))[0]}.mp3")
                transcript_file = os.path.join(config['output_transcripts_directory'], f"{os.path.splitext(os.path.basename(video_file))[0]}.txt")

                # Submit video to audio conversion task
                future = executor.submit(convert_video_to_audio, video_file, audio_file)
                futures.append((future, audio_file, transcript_file))

            # Wait for all conversions in the batch to complete
            for future, audio_file, transcript_file in futures:
                try:
                    future.result()  # Ensure the conversion is complete
                    # Submit transcription task
                    executor.submit(transcribe_audio, audio_file, transcript_file, config['gpu'])
                except Exception as e:
                    logger.error(f"Error processing {audio_file}: {str(e)}")

            logger.info(f"Completed batch. Cooling for {config['cooling_period']} seconds.")
            time.sleep(config['cooling_period'])

    logger.info("All videos processed.")

if __name__ == "__main__":
    main()
