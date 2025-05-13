# Import required libraries
import pyaudio  # Library for accessing and recording audio streams
import time  # Used for tracking recording durations and cooldowns
import speech_recognition as sr  # Library for converting speech to text

# This value is usually controlled by the GUI, but we define a fallback here
listening_duration = 10  # Default listening duration in seconds
cooldown_duration = 3  # Pause after recording to prevent immediate reactivation

def find_vb_cable_device():
    """Searches all audio input devices and returns the index of VB-Cable output."""
    p = pyaudio.PyAudio()  # Initialize PyAudio instance
    device_index = None  # Placeholder for device index

    # Iterate through available audio devices
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)  # Get device info at index i

        # Check if the device is named like a VB-CABLE (virtual audio cable)
        if "CABLE Output" in dev['name']:
            device_index = i  # Save its index
            break  # Stop checking once found

    p.terminate()  # Clean up PyAudio instance
    return device_index  # Return the matching device index or None


def record_audio_vb_cable(duration=3):
    """
    Records raw audio from the VB-CABLE output device for a given duration.
    Returns raw bytes of audio data or None if the device isn't found.
    """
    p = pyaudio.PyAudio()  # Create PyAudio object
    device_index = find_vb_cable_device()  # Find the virtual cable device

    if device_index is None:
        return None  # If device not found, stop the function

    try:
        # Open an audio stream for input using the VB-CABLE device
        stream = p.open(format=pyaudio.paInt16,  # 16-bit resolution
                        channels=1,  # Mono audio
                        rate=16000,  # Sample rate (standard for speech)
                        input=True,
                        frames_per_buffer=1024,  # Buffer size
                        input_device_index=device_index)  # Use VB-CABLE index
    except Exception as e:
        # In case of failure to open the stream, clean up and return None
        p.terminate()
        return None

    frames = []  # List to store recorded audio chunks
    start_time = time.time()  # Note the start time

    # Continue recording until duration is met
    while time.time() - start_time < duration:
        try:
            # Read a chunk of audio data
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)  # Store the audio data
        except IOError:
            break  # If reading fails, break the loop

    # Stop and clean up the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Return all frames joined together as a single bytes object
    return b"".join(frames)


def transcribe_audio(audio_data):
    """
    Uses Google’s Speech Recognition to convert audio to text.
    Accepts raw audio bytes and returns transcribed text.
    """
    recognizer = sr.Recognizer()  # Create a Recognizer instance
    audio = sr.AudioData(audio_data, 16000, 2)  # Wrap raw bytes into AudioData

    try:
        # Try to transcribe using Google Speech Recognition
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "[Unintelligible noise]"  # Could not understand the audio
    except sr.RequestError as e:
        return f"[Error with speech recognition service: {e}]"  # API call error


def listen_and_output(duration=10):
    """
    High-level function to record and transcribe VB-CABLE audio.
    Called from the main program with a given listening duration.
    """
    audio_data = record_audio_vb_cable(duration=duration)  # Record from VB-CABLE

    if audio_data is None:
        return "Error capturing audio."  # If recording failed

    # Transcribe and return the result
    transcription = transcribe_audio(audio_data)
    return transcription


# When the script is run directly (not imported), test the functionality
if __name__ == "__main__":
    result = listen_and_output(duration=5)  # Record for 5 seconds
    print(result)  # Output the transcription
