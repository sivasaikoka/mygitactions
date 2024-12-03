import tempfile
import os
import wave
import speech_recognition as sr
import logging

# Initialize logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def convert_to_pcm_wav(input_file):
    try:
        recognizer = sr.Recognizer()  # Initialize recognizer
        # Load the original audio file
        with sr.AudioFile(input_file) as source:
            audio_data = recognizer.record(source)
            # Generate a temporary WAV file path
            temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_wav_file.close()  # Close the file so we can open it with wave module

            with wave.open(temp_wav_file.name, 'wb') as wav_file:
                wav_file.setnchannels(source.channels)
                wav_file.setsampwidth(recognizer.get_sample_width())
                wav_file.setframerate(source.sample_rate)
                wav_file.writeframes(audio_data.get_wav_data())

            return temp_wav_file.name
    except Exception as e:
        logger.error(f"Error converting audio to PCM WAV: {e}")
        return None
