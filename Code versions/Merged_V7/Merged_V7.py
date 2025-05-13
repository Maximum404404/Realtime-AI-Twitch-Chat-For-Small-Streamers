import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mss
import time
import requests
import random

# Importing the required functions from the individual files
from Screen_Desc import start_capture  # Importing the screen input function
from PyAudio_Desktop import listen_and_output  # Importing PyAudio desktop capture function
from Get_Mic_Input import capture_and_recognize_speech  # Importing mic input function

# Global variables to store process outputs
F1 = ""
F2 = ""
F3 = ""

# Global variables for GUI inputs
background_info = ""
main_topics_and_behavior = ""
selected_monitor_index = None
streamer_username = ""  # Global to hold the username

# Timer variables
timer_running = False
reset_timer_duration = 10  # Default reset duration in seconds
listening_duration = 5  # Default listening duration for desktop audio

# Function to handle the button click and start the sequential processes
def start_program():
    global F1, F2, F3, timer_running, background_info, main_topics_and_behavior, streamer_username

    # Retrieve user inputs from the GUI
    chatgpt_api_key = api_key_entry.get().strip()  # Strip unwanted spaces/newlines
    streamer_username = username_entry.get().strip()  # Get the username

    if not streamer_username:
        messagebox.showwarning("Missing Username", "Please enter your username.")
        return

    # Ensure at least one file is selected
    if not (mic_input_var.get() or screen_input_var.get() or audio_input_var.get()):
        messagebox.showwarning("File Selection", "Please select at least one file to continue.")
        return

    # Ensure monitor is selected if "Screen Input" is enabled
    if screen_input_var.get() and selected_monitor_index is None:
        messagebox.showwarning("Monitor Selection", "Please select a monitor for screen input.")
        return

    # Handle optional inputs from the GUI
    if background_info_toggle_var.get():
        background_info = background_info_entry.get()
    else:
        background_info = ""  # Reset if not toggled

    if topics_toggle_var.get():
        main_topics_and_behavior = topics_entry.get()
    else:
        main_topics_and_behavior = ""  # Reset if not toggled

    # Retrieve timers from the GUI
    try:
        global reset_timer_duration, listening_duration
        reset_timer_duration = int(reset_timer_entry.get())
        listening_duration = int(audio_duration_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter valid numeric values for timers.")
        return

    # Start the loop for sequential execution
    timer_running = True
    threading.Thread(target=sequential_process_execution, args=(chatgpt_api_key,), daemon=True).start()


# Function to execute processes sequentially
def sequential_process_execution(chatgpt_api_key):
    global F1, F2, F3, timer_running

    while timer_running:
        # Process each input type based on toggles
        if mic_input_var.get():
            F1 = capture_mic_input()
            update_combined_output()

        if screen_input_var.get():
            F3 = capture_screen_input()
            update_combined_output()

        if audio_input_var.get():
            F2 = capture_audio_input()
            update_combined_output()

        # Prepare the ChatGPT API prompt
        inputs = "\n".join(filter(None, [F1, F2, F3]))  # Combine non-empty outputs
        prompt = (
            f"Streamer Username: {streamer_username}\n"
            f"{'Background Information: ' + background_info if background_info else ''}\n"
            f"{'Main Topics and Behavior: ' + main_topics_and_behavior if main_topics_and_behavior else ''}\n"
            f"User Input:\n{F1}\n"
            f"Screen Description:\n{F3}\n"
            f"Desktop Audio:\n{F2}\n"
            "Responses must be within 40 and 140 characters\n"
            "Generate a DIFFRENT ABD UNIQUE Response for the streamer to use in their interaction.\n"
            "Do not start a response with Streamer: or StreamerResponse: (Please use common sense)\n"
            "Generate a response for the streamer to use in their interaction. DIFFRENT EACH TIME !!!\n"
            "25% chance the message should also be negative (Such as i hate this stream and / or streamer because...)\n"
            "responses have a 25% chance to do a emoji (Such as :) or even O7)\n"
            "25% chance for each message to contain one of the following phrases Separated by a comma (Pogchamp, Poggers, Pog, Poggies, Hype, W, EZ Clap, Let's gooooo, Sheeeeeesh, Based, POGGERS, PogU, GOAT, GOGOGOGOGO, Big W, That's a W, Rigged, Sadge, PepeHands, OMEGALUL, F, bruh, KEKW, Cringe, Malding, FeelsBadMan, Smh, LUL, FailFish, Yikes, Reeeee, Triggered, AYAYA, MonkaS, MonkaW, Oop, WidePeepoHappy, PeepoG, PogU, 4Weird, KAPPA, Jebaited, SHOCKED, oof, BigF, WutFace, CmonBruh, WOW, LUL, LOLW, xD, ROFL, kek, kekw, OMEGALUL, KEKW, LULW, Hehe, Haha, LULW, Dead, Lulz, Cracked, Tehe, AYAYAYA, UwU, OwO, Awoo, nya~, Kawaii, Cuteness overload, Snuggle, Huggies, Blushing, Purr, Nyan Cat, Poke, Boop, Fluff, Snuggles, Clap, EZ, Pepega, 3Head, DansGame, FeelsWeirdMan, Cringe, F tier, Big L, L dance, Tryhard, XD, Dumb, Sadge, Bonk, Rekt, GetGood, ResidentSleeper, BibleThump, Kappa, WeirdChamp, POGGIES, PepeLaugh, TriHard, POGGERS, MonkaW, Lurk, LULW, Kappapride, Pogo, FeelsOkayMan, SwoleDog, Praying, OMEGALULW, YEP, Hmmm, AYOOO, Zzz, Oops, BOOBA, POGGIES, Bruh, Ok, Nah, Whoa, YOOO, WompWomp, WTF, Scuffed, PepeD, GachiGASM, CatJAM, FeelsGoodMan, FeelsBadMan, NotLikeThis, Clap, CmonBruh, Sussy, PogChamp, PogFist, Big Pog, LULF, Swole, POGGERS, FeelsStrongMan)\n"
            "25% chance the messages should be negative (e.g., 'I hate this stream because...').\n"
            "25% chance to include an emoji (e.g., ':)' or 'O7').\n"
            "25% chance to include a Twitch-style phrase (e.g., PogChamp, KEKW, FeelsBadMan, etc.).\n"
        )
        if chatgpt_enabled_var.get():  # Only call ChatGPT if the toggle is checked
            # Generate dynamic responses
            for _ in range(random.randint(3, 10)):  # Generate 3-10 dynamic responses
                random_username = generate_twitch_style_username(chatgpt_api_key)
                color_code = generate_random_color()
                reset = reset_color()
                gpt_response = send_to_chatgpt_api(chatgpt_api_key, prompt)

                if gpt_response:
                    print(f"{color_code}{random_username}{reset}: {gpt_response}")
        else:
            # If ChatGPT is disabled, just print the combined output
            pass  # Removed the debug print statement for combined output

        # Wait for the reset timer duration before restarting
        time.sleep(reset_timer_duration)


# Function to capture microphone input
def capture_mic_input():
    try:
        prompt = capture_and_recognize_speech()  # Capture and recognize speech once
        if prompt:
            return f"User Input: {prompt}"
        else:
            return "User Input: [No speech detected]"
    except Exception as e:
        return f"User Input: [Error in mic input: {e}]"


# Function to capture audio input
def capture_audio_input():
    try:
        transcription = listen_and_output(duration=listening_duration)  # Capture and transcribe audio input
        return f"Desktop Audio: {transcription}"
    except Exception as e:
        return f"Desktop Audio: [Error in audio input: {e}]"


# Function to capture screen input
def capture_screen_input():
    try:
        result = start_capture(selected_monitor_index)  # Pass the selected monitor index
        return f"Screen Description: {result}"
    except Exception as e:
        return f"Screen Description: [Error in screen input: {e}]"


# Function to send data to the ChatGPT API with retry logic
def send_to_chatgpt_api(chatgpt_api_key, prompt):
    headers = {
        "Authorization": f"Bearer {chatgpt_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-3.5-turbo",  # Changed this from "gpt-4" to "gpt-3.5-turbo"
    }

    max_retries = 2  # Set maximum retry count
    retry_delay = 2  # Wait 5 seconds before retrying

    for attempt in range(max_retries):
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                if response.status_code == 429:
                    time.sleep(retry_delay)
        except Exception as e:
            time.sleep(retry_delay)
    
    return "Error: Unable to get a response from ChatGPT after multiple retries."


# Function to generate a Twitch-style username using GPT-3.5 Turbo API
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


# Function to generate a random color for responses (excluding black/white)
def generate_random_color():
    colors = ['\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[91m', '\033[95m']
    return random.choice(colors)


# Function to reset color
def reset_color():
    return '\033[0m'


# Function to combine the outputs and display them
def update_combined_output():
    combined_output = f"{F1}\n{F2}\n{F3}"  # Use F1, F2, F3 labels for consistency
    combined_output_label.config(text=combined_output)


# Function to enable or disable monitor selection dropdown based on Screen Input toggle
def toggle_screen_input():
    if screen_input_var.get():
        monitor_label.pack(pady=5)
        monitor_combobox.pack(pady=10)
    else:
        monitor_label.pack_forget()
        monitor_combobox.pack_forget()


# Function to handle monitor selection and set the global variable
def on_select_monitor(event=None):
    global selected_monitor_index
    selected_monitor_index = monitor_combobox.current()


# GUI setup
root = tk.Tk()
root.title("Streamer Chatbot")
root.geometry("600x800")

# API Key entry
api_key_label = ttk.Label(root, text="ChatGPT API Key:")
api_key_label.pack(pady=10)
api_key_entry = ttk.Entry(root, width=40)
api_key_entry.pack(pady=5)

# Username entry
username_label = ttk.Label(root, text="Streamer Username:")
username_label.pack(pady=10)
username_entry = ttk.Entry(root, width=40)
username_entry.pack(pady=5)

# ChatGPT Enable toggle
chatgpt_enabled_var = tk.BooleanVar()
chatgpt_enabled_checkbox = ttk.Checkbutton(root, text="Enable ChatGPT", variable=chatgpt_enabled_var)
chatgpt_enabled_checkbox.pack(pady=5)

# Input method toggles
mic_input_var = tk.BooleanVar()
mic_input_checkbox = ttk.Checkbutton(root, text="Mic Input", variable=mic_input_var)
mic_input_checkbox.pack(pady=5)

screen_input_var = tk.BooleanVar()
screen_input_checkbox = ttk.Checkbutton(root, text="Screen Input", variable=screen_input_var, command=toggle_screen_input)
screen_input_checkbox.pack(pady=5)

audio_input_var = tk.BooleanVar()
audio_input_checkbox = ttk.Checkbutton(root, text="Desktop Audio Input", variable=audio_input_var)
audio_input_checkbox.pack(pady=5)

# Monitor selection
monitor_label = ttk.Label(root, text="Select Monitor:")
monitor_combobox = ttk.Combobox(root, values=["Monitor 1", "Monitor 2", "Monitor 3", "Monitor 4"])
monitor_combobox.bind("<<ComboboxSelected>>", on_select_monitor)

# Background info input
background_info_toggle_var = tk.BooleanVar()
background_info_checkbox = ttk.Checkbutton(root, text="Enable Background Info", variable=background_info_toggle_var)
background_info_checkbox.pack(pady=5)

background_info_label = ttk.Label(root, text="Background Info:")
background_info_label.pack(pady=5)
background_info_entry = ttk.Entry(root, width=40)
background_info_entry.pack(pady=5)

# Main topics input
topics_toggle_var = tk.BooleanVar()
topics_toggle_checkbox = ttk.Checkbutton(root, text="Enable Main Topics & Behavior", variable=topics_toggle_var)
topics_toggle_checkbox.pack(pady=5)

topics_label = ttk.Label(root, text="Main Topics and Behavior:")
topics_label.pack(pady=5)
topics_entry = ttk.Entry(root, width=40)
topics_entry.pack(pady=5)

# Timers input
reset_timer_label = ttk.Label(root, text="Reset Timer (seconds):")
reset_timer_label.pack(pady=5)
reset_timer_entry = ttk.Entry(root, width=10)
reset_timer_entry.pack(pady=5)

audio_duration_label = ttk.Label(root, text="Audio Duration (seconds):")
audio_duration_label.pack(pady=5)
audio_duration_entry = ttk.Entry(root, width=10)
audio_duration_entry.pack(pady=5)

# Start button
start_button = ttk.Button(root, text="Start Program", command=start_program)
start_button.pack(pady=20)

# Combined output label
combined_output_label = ttk.Label(root, text="", wraplength=550, justify="left")
combined_output_label.pack(pady=10)

root.mainloop()
