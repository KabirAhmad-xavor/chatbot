import azure.cognitiveservices.speech as speechsdk
import time
import os
import string
from chatbot import chatbot_with_memory
from audio import play_saved_audio
import rospy
from class_keyword_publisher import KeywordPublisher
from dotenv import load_dotenv
import os
# ---------------------- Configuration ----------------------
keyword_publisher = KeywordPublisher()

# Load environment variables from .env file
load_dotenv()
speech_key = os.getenv("SPEECH_KEY")
service_region = "eastus"
keyword_model_path = "e200c66f-b9d4-4f65-ae32-dbca7cea66a4.table"
wake_word = "Companion"


# ---------------------- Command List ----------------------
command_phrases = {
    "stop following me", "stop follow me", "stop following", "pose",
    "come closer", "come close", "come here", "go away",
    "follow me", "move close", "stop", "break"
}

# ---------------------- Check Model File ----------------------
if not os.path.exists(keyword_model_path):
    print(f"❌ ERROR: Model file not found at: {keyword_model_path}")
    exit(1)

# ---------------------- Setup ----------------------
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
keyword_model = speechsdk.KeywordRecognitionModel(keyword_model_path)

# ---------------------- Wake Word Listener ----------------------
def listen_for_wake_word():
    global wake_word_detected

    def on_recognized(evt):
        global wake_word_detected
        if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
            print(f"\n✅ Wake word '{wake_word}' detected!")
            wake_word_detected = True

    def on_canceled(evt):
        #print("❌ Wake word recognition canceled.")
        cancellation_details = speechsdk.CancellationDetails.from_result(evt.result)
        print("Reason:", cancellation_details.reason)
        print("Error Code:", cancellation_details.error_code)
        print("Error Details:", cancellation_details.error_details)

    try:
        while True:
            wake_word_detected = False
            print(f"\n🎤 Listening for wake word: '{wake_word}'...")

            # Create new recognizer instance
            audio_config = speechsdk.AudioConfig(use_default_microphone=True)
            recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            recognizer.recognized.connect(on_recognized)
            recognizer.canceled.connect(on_canceled)

            # Start keyword recognition
            try:
                start_future = recognizer.start_keyword_recognition_async(keyword_model)
                start_future.get()
            except Exception as e:
                print(f"⚠ Failed to start keyword recognition: {e}")
                continue

            # Wait until wake word is detected
            while not wake_word_detected:
                time.sleep(0.5)

            listen_for_command()
            # Stop keyword recognizer after detection
            stop_future = recognizer.stop_keyword_recognition_async()
            stop_future.get()
            #time.sleep(1)

            # Start listening for voice command
            #listen_for_command()

    except KeyboardInterrupt:
        print("\n👋 Exiting on user interrupt.")


# ---------------------- Remove Punctuation  ----------------------
def remove_punctuation(text):
    """Removes punctuation from the input text."""
    return text.translate(str.maketrans('', '', string.punctuation))




# ---------------------- Voice Command Listener ----------------------
def listen_for_command():
    print("🎤 Listening for voice command...")

    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    command_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = command_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = remove_punctuation(result.text.strip().lower())
        
        print(f"🗣 Detected speech: {recognized_text}")

        if recognized_text in command_phrases:
            print("✅ Command detected")
            publish_command(recognized_text)
        else:
            print("ℹ Speech does not match command list")
            response=chatbot_with_memory(result.text.strip().lower(), verbose=False)
            print(response)
            publish_convo(response)
            play_saved_audio(response,output_device_index=2, volume=10)
            


    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("❌ No speech recognized.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speechsdk.CancellationDetails.from_result(result)
        print("❌ Command recognition canceled.")
        print("Reason:", cancellation_details.reason)
        print("Error Details:", cancellation_details.error_details)

# ---------------------- publish convo ----------------------

def publish_convo(text):
    intent = 'interaction'
    keyword_publisher.publish_keyword(intent, text)
    print(f"Interaction Published: {text}")

def publish_command(text):
    intent = 'control'
    print("intent is : ", intent)
    keyword_publisher.publish_keyword(intent, text)
    print(f"Control Published: {text}")

# ---------------------- Main ----------------------


if __name__ == "__main__":
    listen_for_wake_word()
