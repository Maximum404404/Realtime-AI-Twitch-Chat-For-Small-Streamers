import speech_recognition as sr  # Import the speech recognition library correctly

# Function to capture microphone input and recognize speech
def capture_and_recognize_speech():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise to set the baseline energy threshold
        r.energy_threshold = 400  # Set a static energy threshold level (adjust as needed)
        r.dynamic_energy_threshold = True  # Enable dynamic adjustment based on ambient noise levels

        print("Speak now:")  # Prompt the user to speak
        try:
            # Listen for audio input with a timeout of 5 seconds to avoid waiting indefinitely
            audio = r.listen(source, timeout=5)
            # Use Google's speech recognition to convert audio to text
            prompt = r.recognize_google(audio, language="en-EN", show_all=False)
            return prompt  # Return the recognized speech as text
        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return None  # Return None if the speech was not recognized
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return None  # Return None if there was a timeout
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return None  # Return None if there was a service error

# Loop to continuously listen for audio input and respond
if __name__ == "__main__":
    while True:
        prompt = capture_and_recognize_speech()

        if prompt is not None:
            print("You Said:", prompt)  # Display the recognized text
