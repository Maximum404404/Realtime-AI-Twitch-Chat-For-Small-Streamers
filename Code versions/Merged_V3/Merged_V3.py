import tkinter as tk
from tkinter import ttk, messagebox
import threading
import mss

# Importing the required functions from the individual files
from Screen_Desc import start_capture  # Importing the screen input function
from PyAudio_Desktop import listen_and_output  # Importing PyAudio desktop capture function
from Get_Mic_Input import capture_and_recognize_speech  # Importing mic input function

# Global variables to store process states
selected_monitor_index = None

# Variables to store outputs from each file
F1 = ""
F2 = ""
F3 = ""

# Events for managing threading
mic_input_event = threading.Event()
screen_input_event = threading.Event()
audio_input_event = threading.Event()

# Function to handle the button click and start the selected process
def start_program():
    global selected_monitor_index, F1, F2, F3

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

    # Start the processes sequentially, only after the previous one finishes
    if use_mic_input:
        threading.Thread(target=start_mic_input, daemon=True).start()

# Function to start the mic input capture
def start_mic_input():
    global F1
    print("Starting microphone input capture...")
    try:
        prompt = capture_and_recognize_speech()  # Capture and recognize speech once
        if prompt is not None:
            F1 = prompt  # Capture the mic input in F1
            print(f"Mic Input (F1): {F1}")
            update_combined_output()  # Update the combined output
        else:
            print("No speech recognized.")
        
        mic_input_event.set()  # Signal that the mic input has completed
        if mic_input_event.is_set():
            print("Mic input finished. Now starting screen input.")
            threading.Thread(target=start_screen_input, daemon=True).start()  # Start screen input after mic input

    except Exception as e:
        messagebox.showerror("Error", f"Error in mic input: {e}")
        mic_input_event.set()  # Ensure the event is set even in case of error

# Function to start the audio input (VB-Cable) capture
def start_audio_input():
    global F2
    print("Starting audio input capture from VB-Cable...")
    try:
        F2 = listen_and_output()  # Capture the audio input in F2
        print(f"Audio Input (F2): {F2}")
        update_combined_output()  # Update the combined output
    except Exception as e:
        messagebox.showerror("Error", f"Error in audio input: {e}")
    audio_input_event.set()  # Signal that the audio input has completed

# Function to start screen input (with monitor selection)
def start_screen_input():
    global F3
    print("Starting screen input capture...")
    try:
        print(f"Monitor {selected_monitor_index} selected for screen input.")
        F3 = start_capture()  # Capture the screen input in F3
        print(f"Screen Input (F3): {F3}")
        update_combined_output()  # Update the combined output

        screen_input_event.set()  # Signal that the screen input has completed
        if screen_input_event.is_set():
            print("Screen input finished. Now starting audio input.")
            threading.Thread(target=start_audio_input, daemon=True).start()  # Start audio input after screen input

    except Exception as e:
        messagebox.showerror("Error", f"Error in screen input: {e}")
        screen_input_event.set()  # Ensure the event is set even in case of error

# Function to enable or disable monitor selection dropdown based on Screen Input toggle
def toggle_screen_input():
    if screen_input_var.get():
        monitor_combobox.pack(pady=10)  # Show the monitor selection combobox
    else:
        monitor_combobox.pack_forget()  # Hide the monitor selection combobox

# Function to handle monitor selection and set the global variable
def on_select_monitor(event=None):
    global selected_monitor_index
    selected_monitor_index = monitor_combobox.current() + 1  # MSS is 1-indexed
    print(f"Monitor {selected_monitor_index} selected.")  # Debugging message

# Function to combine the outputs and display them
def update_combined_output():
    # Combine the outputs into one statement
    combined_output = f"Mic Input: {F1}\nAudio Input: {F2}\nScreen Input: {F3}"
    print(f"Combined Output:\n{combined_output}")
    combined_output_label.config(text=combined_output)  # Update the label with the combined output

# Create the main window
root = tk.Tk()
root.title("Chatto Code Setup")
root.geometry("500x700")

# Add a label
header_label = tk.Label(root, text="Chatto Code Setup", font=("Arial", 16))
header_label.pack(pady=10)

# API Key entry
api_key_label = tk.Label(root, text="ChatGPT API Key:")
api_key_label.pack(pady=5)
api_key_entry = tk.Entry(root, width=40)
api_key_entry.pack(pady=5)

# Streamer username entry
username_label = tk.Label(root, text="Streamer Username:")
username_label.pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack(pady=5)

# Background info toggle and entry
background_info_toggle_var = tk.BooleanVar(value=False)
background_info_toggle = tk.Checkbutton(root, text="Include Background Information?", variable=background_info_toggle_var)
background_info_toggle.pack(pady=5)

# Main topics toggle and entry
topics_toggle_var = tk.BooleanVar(value=False)
topics_toggle = tk.Checkbutton(root, text="Include Main Topics and Behavior?", variable=topics_toggle_var)
topics_toggle.pack(pady=5)

# GPT version selection
gpt_version_label = tk.Label(root, text="Select GPT Version:")
gpt_version_label.pack(pady=5)
gpt_version_combobox = ttk.Combobox(root, values=["GPT-3", "GPT-4"])
gpt_version_combobox.current(0)
gpt_version_combobox.pack(pady=5)

# File toggle checkboxes
mic_input_var = tk.BooleanVar()
screen_input_var = tk.BooleanVar()
audio_input_var = tk.BooleanVar()

mic_input_checkbox = tk.Checkbutton(root, text="Use Mic Input", variable=mic_input_var)
mic_input_checkbox.pack(pady=5)

screen_input_checkbox = tk.Checkbutton(root, text="Use Screen Input", variable=screen_input_var, command=toggle_screen_input)
screen_input_checkbox.pack(pady=5)

audio_input_checkbox = tk.Checkbutton(root, text="Use Audio Input", variable=audio_input_var)
audio_input_checkbox.pack(pady=5)

# Monitor selection dropdown (hidden by default)
monitor_combobox = ttk.Combobox(root, values=["Monitor 1", "Monitor 2", "Monitor 3"])
monitor_combobox.bind("<<ComboboxSelected>>", on_select_monitor)

# Button to start the program
start_button = tk.Button(root, text="Start", command=start_program)
start_button.pack(pady=20)

# Label for combined output
combined_output_label = tk.Label(root, text="", font=("Arial", 10), justify="left")
combined_output_label.pack(pady=20)

# Run the main loop
root.mainloop()
