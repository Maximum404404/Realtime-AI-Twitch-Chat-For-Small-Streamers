# Import required modules
import tkinter as tk  # GUI module
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for popup alerts
import threading  # To run background tasks concurrently
import mss  # Used for screen capturing (screenshot)
import time  # Time-based operations
import requests  # For sending API requests
import random  # For generating randomness (e.g., response color, emojis, etc.)

# Importing specific functions from local modules
from Screen_Desc import start_capture  # Screen content summarizer
from PyAudio_Desktop import listen_and_output  # Audio transcription from desktop sound
from Get_Mic_Input import capture_and_recognize_speech  # Mic input speech recognizer

# Global variables to hold outputs from each module
F1 = ""  # Microphone input result
F2 = ""  # Desktop audio input result
F3 = ""  # Screen content description

# Globals for user-configured settings
background_info = ""  # Background context for the prompt
main_topics_and_behavior = ""  # Optional behavior and topics for GPT prompt
selected_monitor_index = None  # Index for selected monitor
streamer_username = ""  # Twitch/streamer username for personalization

# State for looped timer function
timer_running = False
reset_timer_duration = 10  # Time to wait between each loop cycle
listening_duration = 5  # Duration of desktop audio capture

# Primary function that starts everything when the "Start Program" button is clicked
def start_program():
    global F1, F2, F3, timer_running, background_info, main_topics_and_behavior, streamer_username

    # Get API key and streamer name from input fields
    chatgpt_api_key = api_key_entry.get().strip()
    streamer_username = username_entry.get().strip()

    # Ensure the username is filled in
    if not streamer_username:
        messagebox.showwarning("Missing Username", "Please enter your username.")
        return

    # At least one input method must be selected
    if not (mic_input_var.get() or screen_input_var.get() or audio_input_var.get()):
        messagebox.showwarning("File Selection", "Please select at least one file to continue.")
        return

    # Require monitor selection if screen input is chosen
    if screen_input_var.get() and selected_monitor_index is None:
        messagebox.showwarning("Monitor Selection", "Please select a monitor for screen input.")
        return

    # Handle toggled background info
    if background_info_toggle_var.get():
        background_info = background_info_entry.get()
    else:
        background_info = ""

    # Handle toggled main topics
    if topics_toggle_var.get():
        main_topics_and_behavior = topics_entry.get()
    else:
        main_topics_and_behavior = ""

    # Safely convert text inputs into integer values
    try:
        global reset_timer_duration, listening_duration
        reset_timer_duration = int(reset_timer_entry.get())
        listening_duration = int(audio_duration_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter valid numeric values for timers.")
        return

    # Begin threaded execution
    timer_running = True
    threading.Thread(target=sequential_process_execution, args=(chatgpt_api_key,), daemon=True).start()


# Looped function that runs all enabled capture functions and sends data to ChatGPT
def sequential_process_execution(chatgpt_api_key):
    global F1, F2, F3, timer_running

    while timer_running:
        # Execute mic input if selected
        if mic_input_var.get():
            F1 = capture_mic_input()
            update_combined_output()

        # Execute screen capture if selected
        if screen_input_var.get():
            F3 = capture_screen_input()
            update_combined_output()

        # Execute desktop audio capture if selected
        if audio_input_var.get():
            F2 = capture_audio_input()
            update_combined_output()

        # Compose full input for ChatGPT
        inputs = "\n".join(filter(None, [F1, F2, F3]))  # Remove empty parts
        prompt = (
            f"Streamer Username: {streamer_username}\n"
            f"{'Background Information: ' + background_info if background_info else ''}\n"
            f"{'Main Topics and Behavior: ' + main_topics_and_behavior if main_topics_and_behavior else ''}\n"
            f"User Input:\n{F1}\n"
            f"Screen Description:\n{F3}\n"
            f"Desktop Audio:\n{F2}\n"
            "Responses must be within 40 and 140 characters\n"
            "Generate a DIFFERENT AND UNIQUE Response for the streamer to use in their interaction.\n"
            "Avoid starting with 'Streamer:' or similar tags.\n"
            "25% chance to be negative\n"
            "25% chance to use an emoji\n"
            "25% chance to use a Twitch phrase from a long predefined list\n"
        )

        # Only send to ChatGPT if enabled
        if chatgpt_enabled_var.get():
            for _ in range(random.randint(3, 10)):  # Generate 3–10 different responses
                random_username = generate_twitch_style_username(chatgpt_api_key)
                color_code = generate_random_color()
                reset = reset_color()
                gpt_response = send_to_chatgpt_api(chatgpt_api_key, prompt)

                if gpt_response:
                    print(f"{color_code}{random_username}{reset}: {gpt_response}")
        else:
            pass  # If disabled, skip API call

        # Wait between each cycle
        time.sleep(reset_timer_duration)


# Capture audio from microphone and return transcript
def capture_mic_input():
    try:
        prompt = capture_and_recognize_speech()
        if prompt:
            return f"User Input: {prompt}"
        else:
            return "User Input: [No speech detected]"
    except Exception as e:
        return f"User Input: [Error in mic input: {e}]"


# Capture and transcribe desktop audio
def capture_audio_input():
    try:
        transcription = listen_and_output(duration=listening_duration)
        return f"Desktop Audio: {transcription}"
    except Exception as e:
        return f"Desktop Audio: [Error in audio input: {e}]"


# Capture screen contents using monitor index
def capture_screen_input():
    try:
        result = start_capture(selected_monitor_index)
        return f"Screen Description: {result}"
    except Exception as e:
        return f"Screen Description: [Error in screen input: {e}]"


# Communicate with ChatGPT API and return generated message
def send_to_chatgpt_api(chatgpt_api_key, prompt):
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-3.5-turbo",  # Currently using GPT-3.5 Turbo
    }

    max_retries = 2
    retry_delay = 2  # Seconds between retries

    for attempt in range(max_retries):
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"].strip()
            elif response.status_code == 429:  # Rate limit
                time.sleep(retry_delay)
        except Exception as e:
            time.sleep(retry_delay)

    return "Error: Unable to get a response from ChatGPT after multiple retries."


# Ask GPT to create a Twitch-style username
def generate_twitch_style_username(chatgpt_api_key):
    prompt = (
        "Generate a unique Twitch-style username suitable for a gaming or streaming platform. "
        "Examples include: Ninja, Shroud, DrLupo, Myth, etc. Feel free to add numbers for uniqueness."
    )

    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-3.5-turbo",
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            username = response.json()["choices"][0]["message"]["content"].strip()
            return username
    except Exception as e:
        return f"Error generating username: {str(e)}"


# Returns a random terminal color code
def generate_random_color():
    colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[91m', '\033[95m']
    return random.choice(colors)

# Returns ANSI reset code to return to normal text
def reset_color():
    return '\033[0m'


# Combines all current inputs and updates the display label in the GUI
def update_combined_output():
    combined_output = f"{F1}\n{F2}\n{F3}"
    combined_output_label.config(text=combined_output)


# Show or hide monitor selection UI based on checkbox
def toggle_screen_input():
    if screen_input_var.get():
        monitor_label.pack(pady=5)
        monitor_combobox.pack(pady=10)
    else:
        monitor_label.pack_forget()
        monitor_combobox.pack_forget()


# Store the user's selected monitor index from dropdown
def on_select_monitor(event=None):
    global selected_monitor_index
    selected_monitor_index = monitor_combobox.current()


# ------------------------- GUI Initialization Section -------------------------

# Initialize the main application window
root = tk.Tk()
root.title("Streamer Chatbot")
root.geometry("600x800")

# API Key
api_key_label = ttk.Label(root, text="ChatGPT API Key:")
api_key_label.pack(pady=10)
api_key_entry = ttk.Entry(root, width=40)
api_key_entry.pack(pady=5)

# Streamer Username
username_label = ttk.Label(root, text="Streamer Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(root, width=40)
username_entry.pack(pady=5)

# Enable ChatGPT
chatgpt_enabled_var = tk.BooleanVar()
chatgpt_enabled_checkbox = ttk.Checkbutton(root, text="Enable ChatGPT", variable=chatgpt_enabled_var)
chatgpt_enabled_checkbox.pack(pady=5)

# Input Method Toggles
mic_input_var = tk.BooleanVar()
mic_input_checkbox = ttk.Checkbutton(root, text="Mic Input", variable=mic_input_var)
mic_input_checkbox.pack(pady=5)

screen_input_var = tk.BooleanVar()
screen_input_checkbox = ttk.Checkbutton(root, text="Screen Input", variable=screen_input_var, command=toggle_screen_input)
screen_input_checkbox.pack(pady=5)

audio_input_var = tk.BooleanVar()
audio_input_checkbox = ttk.Checkbutton(root, text="Desktop Audio Input", variable=audio_input_var)
audio_input_checkbox.pack(pady=5)

# Monitor Dropdown (hidden until enabled)
monitor_label = ttk.Label(root, text="Select Monitor:")
monitor_combobox = ttk.Combobox(root, values=["Monitor 1", "Monitor 2", "Monitor 3", "Monitor 4"])
monitor_combobox.bind("<<ComboboxSelected>>", on_select_monitor)

# Optional Background Info
background_info_toggle_var = tk.BooleanVar()
background_info_checkbox = ttk.Checkbutton(root, text="Enable Background Info", variable=background_info_toggle_var)
background_info_checkbox.pack(pady=5)

background_info_label = ttk.Label(root, text="Background Info:")
background_info_label.pack(pady=5)
background_info_entry = ttk.Entry(root, width=40)
background_info_entry.pack(pady=5)

# Optional Topics
topics_toggle_var = tk.BooleanVar()
topics_toggle_checkbox = ttk.Checkbutton(root, text="Enable Main Topics & Behavior", variable=topics_toggle_var)
topics_toggle_checkbox.pack(pady=5)

topics_label = ttk.Label(root, text="Main Topics and Behavior:")
topics_label.pack(pady=5)
topics_entry = ttk.Entry(root, width=40)
topics_entry.pack(pady=5)

# Timers
reset_timer_label = ttk.Label(root, text="Reset Timer (seconds):")
reset_timer_label.pack(pady=5)
reset_timer_entry = ttk.Entry(root, width=10)
reset_timer_entry.pack(pady=5)

audio_duration_label = ttk.Label(root, text="Audio Duration (seconds):")
audio_duration_label.pack(pady=5)
audio_duration_entry = ttk.Entry(root, width=10)
audio_duration_entry.pack(pady=5)

# Start Button
start_button = ttk.Button(root, text="Start Program", command=start_program)
start_button.pack(pady=20)

# Combined Output Display
combined_output_label = ttk.Label(root, text="", wraplength=550, justify="left")
combined_output_label.pack(pady=10)

# Launch the GUI
root.mainloop()
