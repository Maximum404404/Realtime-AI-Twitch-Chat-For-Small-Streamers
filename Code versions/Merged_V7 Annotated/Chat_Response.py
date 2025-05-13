# Import required libraries
import random  # For generating random choices (e.g., usernames, delay)
import requests  # For making HTTP requests to the ChatGPT API
import time  # Used for adding delays
import speech_recognition as sr  # Used for speech-to-text conversion

# === USER CONFIGURATION SECTION ===

# Ask the user to input their ChatGPT API key for authentication
chatgpt_api_key = input("Enter your ChatGPT API key: ")

# Ask for the streamer's username; used in the prompt personalization
streamer_username = input("What is your streamer username? Remember it for future interactions: ")

# Ask if background info should be included to provide extra context
include_background_info = input("Do you want to include background information about yourself? (yes/no): ")

# Initialize background info (can remain empty)
background_info = ""
if include_background_info.lower() == "yes":
    # If user wants to include it, prompt them
    background_info = input("Please provide background information about yourself: ")

# Ask the user what topics or behavior they want to guide the AI's responses
main_topics_and_behavior = input("Enter main topics and how you want the chat to act: ")

# === FUNCTION DEFINITIONS SECTION ===

# Generate a Twitch-style username using GPT-4 via OpenAI API
def generate_twitch_style_username():
    prompt = (
        "Generate a unique Twitch-style username suitable for a gaming or streaming platform. "
        "The name should be punchy, memorable, and follow the aesthetic of other Twitch usernames. "
        "Numbers should not be at the start of the name, should be starting with a letter "
        "Examples include: Ninja, Shroud, DrLupo, Myth, and more. Feel free to add numbers or slight variations for uniqueness."
    )

    # Define headers including authorization key
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",
        "Content-Type": "application/json",
    }

    # Create payload with prompt and model
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4"
    }

    # Send POST request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    # If successful, parse and return username
    if response.status_code == 200:
        response_data = response.json()
        username = response_data["choices"][0]["message"]["content"].strip()
        return username
    else:
        # Fallback if request fails
        return "Streamer123"

# Generate random ANSI terminal color codes (excluding black and white)
def generate_random_color():
    colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[91m', '\033[95m']
    return random.choice(colors)

# Return ANSI code to reset terminal text color
def reset_color():
    return '\033[0m'

# Generate a message for Twitch chat using user input and context
def generate_dynamic_message(topic, title, user_input):
    prompt = (
        f"Generate a casual and short Twitch chat message related to the topic '{topic}', "
        f"the stream title '{title}', and the user's input '{user_input}'. Make it sound like a "
        f"real viewer interacting in the chat with enthusiasm or humor."
    )

    # Prepare headers and payload for OpenAI API
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-4"
    }

    # Make the request and return the trimmed response
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        response_text = response_data["choices"][0]["message"]["content"]
        return response_text.strip()[:125]  # Limit to 125 chars
    else:
        # Default fallback message
        return f"Couldn't generate a message, but {topic} is awesome!"

# Capture and transcribe microphone input using SpeechRecognition
def capture_and_recognize_speech():
    with sr.Microphone() as source:
        # Adjust microphone sensitivity based on ambient noise
        r.adjust_for_ambient_noise(source)
        r.energy_threshold = 400  # Can be tuned manually
        r.dynamic_energy_threshold = True  # Let it auto-adjust in real time

        print("Speak now:")
        try:
            # Listen for up to 5 seconds for speech
            audio = r.listen(source, timeout=5)
            # Use Google Web Speech API to transcribe
            prompt = r.recognize_google(audio, language="en-EN", show_all=False)
            return prompt
        except sr.UnknownValueError:
            print("Sorry, I didn't get that.")
            return None
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            return None

# === MAIN LOOP ===

# Create a recognizer object globally
r = sr.Recognizer()

# Loop indefinitely, processing speech and generating Twitch-style messages
while True:
    # Capture mic input
    prompt = capture_and_recognize_speech()

    if prompt is not None:
        print("You Said:", prompt)

        # Generate and print multiple (3–10) dynamic viewer-style messages
        for _ in range(random.randint(3, 10)):
            random_username = generate_twitch_style_username()
            color_code = generate_random_color()
            reset = reset_color()
            message = generate_dynamic_message(main_topics_and_behavior, streamer_username, prompt)
            print(f"{color_code}{random_username}{reset}: {message}")

        # Add a delay before listening again (to feel like real Twitch chat)
        wait_seconds = random.uniform(1, 3)
        print(f"Waiting for {wait_seconds:.2f} seconds...")
        time.sleep(wait_seconds)
