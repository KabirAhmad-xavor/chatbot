import os
import sounddevice as sd
import numpy as np
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Directory for saving audio files
AUDIO_SAVE_PATH = "saved_audio"
os.makedirs(AUDIO_SAVE_PATH, exist_ok=True)

def save_audio(phrase, filename="output.wav"):
    """Generate speech using ElevenLabs and save it as a WAV file."""
    if not ELEVENLABS_API_KEY:
        raise ValueError("API key is missing! Please provide a valid ElevenLabs API key.")

    # Initialize ElevenLabs client
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    # Generate speech in MP3 format (since WAV requires a Pro plan)
    audio_stream = client.text_to_speech.convert(
        text=phrase,
        voice_id="XrExE9yKIg1WjnnlVkGX",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128"  # Generate MP3 (convert to WAV later) 
    )

    # Read audio data
    audio_bytes = b"".join(audio_stream)

    # Save as MP3
    mp3_path = os.path.join(AUDIO_SAVE_PATH, filename.replace(".wav", ".mp3"))
    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)

    # Convert MP3 to WAV (for better playback control)
    sound = AudioSegment.from_mp3(mp3_path)
    wav_path = os.path.join(AUDIO_SAVE_PATH, filename)
    sound.export(wav_path, format="wav")

    print(f"✅ Audio saved at: {wav_path}")
    return wav_path  # Return the saved WAV file path

# def play_saved_audio(text,output_device_index=5, volume=10):
#     """Play a saved WAV audio file with volume control."""
#     # Load the WAV file using pydub
    
#     file_path = save_audio(text, filename="test_audio.wav")

#     sound = AudioSegment.from_wav(file_path)

#     # Reduce volume (default 30% of original)
#     sound = sound - (20 * np.log10(100 / volume))  # Reduce dB by ratio

#     # Ensure correct audio format
#     sound = sound.set_frame_rate(44100).set_channels(2)  # Convert to stereo 44.1kHz

#     # Convert to numpy array
#     samples = np.array(sound.get_array_of_samples(), dtype=np.int16)

#     # Handle stereo audio correctly
#     if sound.channels == 2:
#         samples = samples.reshape(-1, 2)  # Reshape for stereo playback

#     # Normalize to float32 for sounddevice
#     samples = samples.astype(np.float32) / 32768.0

#     # Play the audio using sounddevice
#     try:
#         print(f"🔊 Playing on device {output_device_index} at {volume}% volume...")
#         sd.play(samples, samplerate=sound.frame_rate, device=output_device_index)
#         sd.wait()  # Wait until playback finishes
#         print("✅ Audio playback finished.")
#     except Exception as e:
#         print(f"❌ Error playing audio: {e}")

import threading
import time
import sys

def wait_for_enter_and_stop():
    """Wait for Enter key press and stop audio."""
    input("🔘 Press ENTER anytime to stop playback...\n")
    print("⏹ Stopping audio...")
    sd.stop()

def play_saved_audio(text, output_device_index=5, volume=10):
    """Play a saved WAV audio file with volume control. Stop on Enter key press."""
    file_path = save_audio(text, filename="test_audio.wav")
    sound = AudioSegment.from_wav(file_path)
    sound = sound - (20 * np.log10(100 / volume))
    sound = sound.set_frame_rate(44100).set_channels(2)
    samples = np.array(sound.get_array_of_samples(), dtype=np.int16)

    if sound.channels == 2:
        samples = samples.reshape(-1, 2)

    samples = samples.astype(np.float32) / 32768.0

    try:
        print(f"🔊 Playing on device {output_device_index} at {volume}% volume...")

        # Start background thread to listen for Enter key
        enter_thread = threading.Thread(target=wait_for_enter_and_stop, daemon=True)
        enter_thread.start()

        sd.play(samples, samplerate=sound.frame_rate, device=output_device_index)
        sd.wait()
        print("✅ Audio playback finished.")
    except Exception as e:
        print(f"❌ Error playing audio: {e}")
