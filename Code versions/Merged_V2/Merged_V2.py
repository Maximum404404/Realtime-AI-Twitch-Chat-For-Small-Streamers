import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mss

# Importing the required functions from the individual files
from Screen_Desc import start_capture  # Importing the screen input function
from PyAudio_Desktop import listen_and_output  # Importing PyAudio desktop capture function

# Global variables to store process states
selected_monitor_index = None

# Function to handle the button click and start the selected process
def start_program():
    global selected_monitor_index

    # Retrieve user inputs from the GUI
    chatgpt_api_key = api_key_entry.get()
    streamer_username = username_entry.get()

    # Check if Background Info and Main Topics should be included
    include_background_info = background_info_toggle_var.get()
    include_main_topics = topics_toggle_var.get()

    # If the toggle is Yes, include the input; otherwise, use an empty string
    background_info = background_info_entry.get() if include_background_info else ""
    main_topics_and_behavior = topics_entry.get() if include_main_topics else ""

    gpt_version = gpt_version_combobox.get()

    # Toggle the files based on the checkbox selections
    use_mic_input = mic_input_var.get()
    use_screen_input = screen_input_var.get()
    use_audio_input = audio_input_var.get()

    # Ensure at least one file is selected
    if not (use_mic_input or use_screen_input or use_audio_input):
        messagebox.showwarning("File Selection", "Please select at least one file to continue.")
        return

    # If "Screen Input" is selected, ensure monitor is selected
    if use_screen_input and selected_monitor_index is None:
        messagebox.showwarning("Monitor Selection", "Please select a monitor for screen input.")
        return

    # Start processes based on the selected checkboxes
    if use_mic_input:
        threading.Thread(target=start_mic_input, daemon=True).start()

    if use_screen_input:
        threading.Thread(target=start_screen_input, daemon=True).start()

    if use_audio_input:
        threading.Thread(target=start_audio_input, daemon=True).start()

    # Debugging print statements
    print(f"Starting with the following settings:")
    print(f"ChatGPT API Key: {chatgpt_api_key}")
    print(f"Streamer Username: {streamer_username}")
    print(f"Background Info: {background_info}")
    print(f"Main Topics and Behavior: {main_topics_and_behavior}")
    print(f"GPT Version: {gpt_version}")
    print(f"Mic Input: {use_mic_input}")
    print(f"Screen Input: {use_screen_input}")
    print(f"Audio Input: {use_audio_input}")

# Function to start the mic input capture
def start_mic_input():
    print("Starting microphone input capture...")
    try:
        while True:
            prompt = capture_and_recognize_speech()
            if prompt is not None:
                print(f"Mic Input: {prompt}")
    except Exception as e:
        messagebox.showerror("Error", f"Error in mic input: {e}")

# Function to start the audio input (VB-Cable) capture
def start_audio_input():
    print("Starting audio input capture from VB-Cable...")
    try:
        listen_and_output()  # Calls the `listen_and_output` from PyAudio_Desktop
    except Exception as e:
        messagebox.showerror("Error", f"Error in audio input: {e}")

# Function to start screen input (with monitor selection)
def start_screen_input():
    print("Starting screen input capture...")
    try:
        print(f"Monitor {selected_monitor_index} selected for screen input.")
        start_capture()  # Calls the `start_capture` from `Screen_Desc.py`
    except Exception as e:
        messagebox.showerror("Error", f"Error in screen input: {e}")

# Function to enable or disable monitor selection dropdown based on Screen Input toggle
def toggle_screen_input():
    print("Toggling screen input...")
    if screen_input_var.get():
        monitor_combobox.pack(pady=10)  # Show the monitor selection combobox
    else:
        monitor_combobox.pack_forget()  # Hide the monitor selection combobox

# Function to handle monitor selection and set the global variable
def on_select_monitor(event=None):
    global selected_monitor_index
    selected_monitor_index = monitor_combobox.current() + 1  # MSS is 1-indexed
    print(f"Monitor {selected_monitor_index} selected.")  # Debugging message

# Create the main window
root = tk.Tk()
root.title("Chatto Code Setup")
root.geometry("400x600")  # Increased the height for additional content

# Add an option for fullscreen toggle
def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))
    return "break"

root.bind("<F11>", toggle_fullscreen)

# Add a label
header_label = tk.Label(root, text="Chatto Code Setup", font=("Arial", 16))
header_label.pack(pady=10)

# API Key entry
api_key_label = tk.Label(root, text="ChatGPT API Key:")
api_key_label.pack(pady=5)
api_key_entry = tk.Entry(root, width=40)
api_key_entry.pack(pady=5)
api_key_entry.insert(0, "Enter your ChatGPT API key here...")  # Placeholder

# Streamer username entry
username_label = tk.Label(root, text="Streamer Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack(pady=5)

# Background info toggle and entry
background_info_toggle_var = tk.BooleanVar(value=False)  # Default to No
background_info_toggle = tk.Checkbutton(root, text="Include Background Information?", variable=background_info_toggle_var)
background_info_toggle.pack(pady=5)
background_info_label = tk.Label(root, text="Background Information:")
background_info_label.pack(pady=5)
background_info_entry = tk.Entry(root, width=40)
background_info_entry.pack(pady=5)

# Main topics toggle and entry
topics_toggle_var = tk.BooleanVar(value=False)  # Default to No
topics_toggle = tk.Checkbutton(root, text="Include Main Topics and Behavior?", variable=topics_toggle_var)
topics_toggle.pack(pady=5)
topics_label = tk.Label(root, text="Main Topics and Behavior:")
topics_label.pack(pady=5)
topics_entry = tk.Entry(root, width=40)
topics_entry.pack(pady=5)

# GPT version selection
gpt_version_label = tk.Label(root, text="Select GPT Version:")
gpt_version_label.pack(pady=5)
gpt_version_combobox = ttk.Combobox(root, values=["GPT-3", "GPT-4"])
gpt_version_combobox.current(0)  # Default to GPT-3
gpt_version_combobox.pack(pady=5)

# File toggle checkboxes
mic_input_var = tk.BooleanVar()
screen_input_var = tk.BooleanVar()
audio_input_var = tk.BooleanVar()

mic_input_checkbox = tk.Checkbutton(root, text="Use Mic Input", variable=mic_input_var)
mic_input_checkbox.pack(pady=5)

# Screen Input checkbox with monitor dropdown below it
screen_input_checkbox = tk.Checkbutton(root, text="Use Screen Input", variable=screen_input_var, command=toggle_screen_input)
screen_input_checkbox.pack(pady=5)

# Dropdown to select the monitor (initially hidden)
monitor_label = tk.Label(root, text="Select Monitor:")
monitor_label.pack_forget()  # Initially hidden

# List monitors and populate the combobox
with mss.mss() as sct:
    monitors = sct.monitors[1:]  # Skip the first item as it's the entire display
    monitor_names = [f"Monitor {i+1}" for i in range(len(monitors))]

# Monitor combobox for selecting monitor
monitor_combobox = ttk.Combobox(root, values=monitor_names)
monitor_combobox.current(0)  # Default to first monitor
monitor_combobox.bind("<<ComboboxSelected>>", on_select_monitor)

# Audio Input checkbox
audio_input_checkbox = tk.Checkbutton(root, text="Use Audio Input (VB-Cable)", variable=audio_input_var)
audio_input_checkbox.pack(pady=5)

# Start button
start_button = tk.Button(root, text="Start", command=start_program)
start_button.pack(pady=20)

# Main loop to run the window
root.mainloop()
