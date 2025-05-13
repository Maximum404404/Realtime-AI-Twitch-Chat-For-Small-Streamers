# Import the SpeechRecognition library for capturing and processing microphone input
import speech_recognition as sr  # Provides tools to convert speech to text

# Function to capture microphone input and recognize speech
def capture_and_recognize_speech():
    r = sr.Recognizer()  # Create an instance of the Recognizer class
    
    # Use the system's default microphone as the audio source
    with sr.Microphone() as source:
        # Adjust the recognizer sensitivity to ambient noise
        r.adjust_for_ambient_noise(source)  # Calibrate energy threshold based on background noise
        
        # Optional manual override of threshold settings
        r.energy_threshold = 400  # Minimum volume level to qualify as speech (can be tuned)
        r.dynamic_energy_threshold = True  # Let the recognizer continue to adapt threshold dynamically

        print("Speak now...")  # Prompt the user to start speaking

        try:
            # Listen for speech, with a timeout to prevent indefinite waiting
            audio = r.listen(source, timeout=5)  # Wait for up to 5 seconds for speech input
            
            # Attempt to recognize the captured audio using Google's free web API
            prompt = r.recognize_google(audio, language="en-EN", show_all=False)
            return prompt  # Return the recognized text as the result

        except sr.UnknownValueError:
            # Triggered when the audio is detected but can't be understood
            print("Sorry, I didn't get that.")
            return None  # Return None to indicate unrecognized speech

        except sr.WaitTimeoutError:
            # Triggered when no speech is detected within the timeout window
            print("Timeout: No speech detected.")
            return None  # Return None for timeout

        except sr.RequestError as e:
            # Triggered if there's an issue connecting to the Google API
            print(f"Error with the speech recognition service; {e}")
            return None  # Return None for API error


# Entry point for running this script directly (e.g., via terminal)
if __name__ == "__main__":
    print("Starting speech recognition...")  # Notify user the script is starting
    
    # Run the microphone capture function
    prompt = capture_and_recognize_speech()
    
    # Output result depending on success or failure
    if prompt:
        print(f"You said: {prompt}")  # Output the recognized text
    else:
        print("No valid speech was recognized.")  # Handle failed recognition
