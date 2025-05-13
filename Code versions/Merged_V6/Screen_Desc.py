import tkinter as tk
from tkinter import ttk
import mss
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the BLIP model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

# Global variable to hold the selected monitor index
selected_monitor_index = 0

# Function to generate a description using BLIP
def get_image_description(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    
    # Generate the output
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_length=90,
            min_length=10,
            num_beams=2,
            length_penalty=1.0,
            early_stopping=True,
            no_repeat_ngram_size=2
        )
    
    description = processor.decode(outputs[0], skip_special_tokens=True)
    return description

# Function to capture, process, and describe the screen content once
def start_capture(monitor_index):  # Accepts monitor_index as argument
    global selected_monitor_index
    selected_monitor_index = monitor_index  # Use the passed index
    return capture_and_describe_once()  # Call the actual function for screen description

# Function to capture and describe the screen content
def capture_and_describe_once():
    global selected_monitor_index
    print("Starting single screen capture...")  # Debugging message
    
    # Start the MSS screen capture session
    with mss.mss() as sct:
        monitor = sct.monitors[selected_monitor_index]
        
        # Capture the screen of the selected monitor
        print(f"Capturing monitor {selected_monitor_index}")  # Debugging message
        screenshot = sct.grab(monitor)
        
        # Convert the screenshot to an image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        # Generate description for the captured image
        description = get_image_description(img)
        
        # Print the description
        print(f"Description: {description}")
        return description

# Function to select monitor
def select_monitor_popup():
    def on_select(event):
        global selected_monitor_index
        selected_monitor_index = monitor_combobox.current() + 1  # MSS is 1-indexed
        print(f"Monitor {selected_monitor_index} selected.")  # Debugging message
        root.destroy()

    # Initialize Tkinter
    root = tk.Tk()
    root.title("Select Monitor")

    # Label and dropdown for monitor selection
    label = tk.Label(root, text="Select Monitor:")
    label.pack(pady=5)

    # List monitors and populate the combobox
    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # Skip the first item as it's the entire display
        monitor_names = [f"Monitor {i+1}" for i in range(len(monitors))]

    # Dropdown to select the monitor
    monitor_combobox = ttk.Combobox(root, values=monitor_names)
    monitor_combobox.current(0)  # Default to first monitor
    monitor_combobox.bind("<<ComboboxSelected>>", on_select)
    monitor_combobox.pack(pady=10)

    root.mainloop()
    print("Monitor selection completed.")  # Debugging message

if __name__ == "__main__":
    select_monitor_popup()  # Show monitor selection popup
    start_capture(selected_monitor_index)  # Start screen capture with selected monitor index
