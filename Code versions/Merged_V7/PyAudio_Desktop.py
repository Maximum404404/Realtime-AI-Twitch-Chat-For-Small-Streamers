import pyaudio
import time
import speech_recognition as sr

# Global variable for listening duration, set by the GUI
listening_duration = 10  # Default to 10 seconds if not set
cooldown_duration = 3  # Cooldown after listening (seconds)

def find_vb_cable_device():
    """Find the VB-Cable output device."""
    p = pyaudio.PyAudio()
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if "CABLE Output" in dev['name']:  # Check for VB-Audio Cable Output
            device_index = i
            break
    p.terminate()
    return device_index

def record_audio_vb_cable(duration=3):
    """Record audio from VB-Cable."""
    p = pyaudio.PyAudio()
    device_index = find_vb_cable_device()
    if device_index is None:
        return None

    try:
        # Open the audio stream with the specified sample rate and mono input
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,  # Mono channel
                        rate=22000,   # Standard sample rate for speech recognition
                        input=True,
                        frames_per_buffer=1024,
                        input_device_index=device_index)
    except Exception as e:
        p.terminate()
        return None

    frames = []
    start_time = time.time()
    while time.time() - start_time < duration:  # Listen for the specified duration
        try:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        except IOError:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    return b"".join(frames)

def transcribe_audio(audio_data):
    """Transcribe audio data to text using SpeechRecognition."""
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, 16000, 2)  # Mono (1 channel) with 16000 Hz

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible noise]"
    except sr.RequestError as e:
        return f"[Error with speech recognition service: {e}]"

def listen_and_output(duration=10):  # Accept duration as argument
    """Capture audio once and output transcription."""
    audio_data = record_audio_vb_cable(duration=duration)  # Use the duration passed
    if audio_data is None:
        return "Error capturing audio."

    transcription = transcribe_audio(audio_data)
    return transcription  # Only return the transcription, no extra prints

# Test the function if running directly
if __name__ == "__main__":
    result = listen_and_output(duration=5)  # Default to 5 seconds for testing
    print(result)  # Only print the final result
