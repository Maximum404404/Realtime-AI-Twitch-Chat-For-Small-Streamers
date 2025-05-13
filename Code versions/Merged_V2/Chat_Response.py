import random
import requests
import time
import speech_recognition as sr  # Import the speech recognition library correctly

# API Key for OpenAI
# Ask the user for their ChatGPT API key
# sk-mK3uzQXzOX-2jdD6r24IOKCRcO-uGiMts6kTxGkV-MT3BlbkFJ8dZ-kn0jxdeKX9WSULHx8gdW04mOYTUiarlY3UiAIA

chatgpt_api_key = input("Enter your ChatGPT API key: ")

# Ask the user for their streamer username, which will be used in the chat interaction
streamer_username = input("What is your streamer username? Remember it for future interactions: ")

# Ask if the user wants to include background information about themselves
include_background_info = input("Do you want to include background information about yourself? (yes/no): ")

background_info = ""
if include_background_info.lower() == "yes":
    # If the user wants to include background information, prompt them for it
    background_info = input("Please provide background information about yourself: ")

# Ask the user to input the main topics they want to discuss and how they want the chat to behave
main_topics_and_behavior = input("Enter main topics and how you want the chat to act: ")

# Function to generate a Twitch-style username using GPT-4 API
def generate_twitch_style_username():
    # Define the prompt to generate a Twitch-style username
    prompt = (
        "Generate a unique Twitch-style username suitable for a gaming or streaming platform. "
        "The name should be punchy, memorable, and follow the aesthetic of other Twitch usernames. "
        "Numbers should not be at the start of the name, should be starting with a letter "
        "Examples include: Ninja, Shroud, DrLupo, Myth, and more. Feel free to add numbers or slight variations for uniqueness."
        
    )

    # Prepare the headers for the API request to OpenAI
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",  # Include the API key for authentication
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Prepare the data payload for the API request
    data = {
        "messages": [
            {"role": "user", "content": prompt}  # Send the prompt to the model
        ],
        "model": "gpt-4"  # Specify the model as GPT-4
    }

    # Send the API request to OpenAI's ChatGPT endpoint
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()  # Parse the JSON response from the API
        username = response_data["choices"][0]["message"]["content"].strip()  # Extract the generated username
        return username
    else:
        # Return a default message if the API call fails
        return "Streamer123"

# Function to generate a random color for the username (excluding black and white)
def generate_random_color():
    colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[91m', '\033[95m']
    return random.choice(colors)

# Function to reset the color back to white
def reset_color():
    return '\033[0m'

# Function to dynamically generate a random message based on the user's input and stream topic
def generate_dynamic_message(topic, title, user_input):
    # Simplify the message prompt to focus on generating Twitch-like chat messages
    prompt = (
        f"Generate a casual and short Twitch chat message related to the topic '{topic}', "
        f"the stream title '{title}', and the user's input '{user_input}'. Make it sound like a "
        f"real viewer interacting in the chat with enthusiasm or humor."
    )

    # Prepare the headers for the API request to OpenAI
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",  # Include the API key for authentication
        "Content-Type": "application/json",  # Specify the content type as JSON
    }

    # Prepare the data payload for the API request
    data = {
        "messages": [
            {"role": "user", "content": prompt}  # Send the prompt to the model
        ],
        "model": "gpt-4"  # Specify the model as GPT-4
    }

    # Send the API request to OpenAI's ChatGPT endpoint
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()  # Parse the JSON response from the API
        response_text = response_data["choices"][0]["message"]["content"]  # Extract the chatbot's response text
        return response_text.strip()[:125]  # Limit response to 125 characters
    else:
        # Return a default message if the API call fails
        return f"Couldn't generate a message, but {topic} is awesome!"

# Function to capture microphone input and recognize speech
def capture_and_recognize_speech():
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

# Create a speech recognizer object to process the audio input
r = sr.Recognizer()

# Loop to continuously listen for audio input and respond
while True:
    prompt = capture_and_recognize_speech()

    if prompt is not None:
        print("You Said:", prompt)  # Display the recognized text

        # Generate a random number of times to display the response (between 3 and 10)
        for _ in range(random.randint(3, 10)):
            random_username = generate_twitch_style_username()  # Generate a username
            color_code = generate_random_color()  # Generate a color
            reset = reset_color()  # Reset color after username
            
            # Generate a dynamic message based on the user's input, stream title, and main topics
            message = generate_dynamic_message(main_topics_and_behavior, streamer_username, prompt)
            
            # Format and display the response
            print(f"{color_code}{random_username}{reset}: {message}")

        # Generate a random delay between 1 to 3 seconds before the next loop iteration
        wait_seconds = random.uniform(1, 3)
        print(f"Waiting for {wait_seconds:.2f} seconds...")
        time.sleep(wait_seconds)  # Pause execution for the generated duration
