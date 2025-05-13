import pyaudio
import numpy as np
import time
import speech_recognition as sr

def find_vb_cable_device():
    """Find the VB-Cable output device."""
    p = pyaudio.PyAudio()
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "CABLE Output" in dev['name']:  # Check for VB-Audio Cable Output
            device_index = i
            print(f"Selected VB-Cable device: {dev['name']}")
            break
    p.terminate()
    return device_index

def record_audio_vb_cable(duration=5):
    """Record audio from VB-Cable."""
    p = pyaudio.PyAudio()
    device_index = find_vb_cable_device()
    if device_index is None:
        print("VB-Cable device not found. Please check your setup.")
        return None

    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,  # Use mono for speech recognition
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024,
                        input_device_index=device_index)
    except Exception as e:
        print(f"Failed to open VB-Cable audio stream: {e}")
        p.terminate()
        return None

    print("Recording audio from VB-Cable (Virtual Cable)...")
    frames = []
    for _ in range(int(44100 / 1024 * duration)):
        try:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        except IOError as e:
            print(f"Error while reading audio data: {e}")
            break

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return b"".join(frames)

def transcribe_audio(audio_data):
    """Transcribe audio data to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, 44100, 2)  # Use stereo input

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible noise]"
    except sr.RequestError as e:
        return f"[Error with speech recognition service: {e}]"

def listen_and_output():
    """Continuously listen to audio and output transcriptions."""
    while True:
        audio_data = record_audio_vb_cable()
        if audio_data is None:
            print("Error capturing audio. Exiting.")
            break

        transcription = transcribe_audio(audio_data)
        print(f"Transcription: {transcription}")
        time.sleep(2)

if __name__ == "__main__":
    listen_and_output()
