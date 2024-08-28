import whisper
import logging

def transcribe_audio(audio_file, transcript_file, use_gpu=False):
    logger = logging.getLogger(__name__)
    try:
        model = whisper.load_model("base", device="cuda" if use_gpu else "cpu")
        result = model.transcribe(audio_file)
        
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        logger.info(f"Successfully transcribed {audio_file} to {transcript_file}")
    except Exception as e:
        logger.error(f"Error transcribing {audio_file}: {str(e)}")
        raise