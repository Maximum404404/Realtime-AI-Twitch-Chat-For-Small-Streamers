# Import necessary libraries
import tkinter as tk  # For GUI elements
from tkinter import ttk  # For themed widgets like Combobox
import mss  # For taking screenshots across multiple monitors
from PIL import Image  # For image processing
import torch  # For running deep learning models
from transformers import BlipProcessor, BlipForConditionalGeneration  # For image captioning using BLIP

# Load the BLIP (Bootstrapped Language-Image Pretraining) model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"  # Automatically use GPU if available, else CPU
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")  # Tokenizer + preprocessing
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)  # Captioning model

# Global variable to track which monitor to capture
selected_monitor_index = 0  # Default to primary monitor

# Function to generate a textual description for an input image using BLIP
def get_image_description(image):
    # Convert image into input tensor format
    inputs = processor(images=image, return_tensors="pt").to(device)
    
    # Generate text description using the model, in inference mode
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=90,  # Limit the length of the generated description
            min_length=10,  # Minimum caption length
            num_beams=2,  # Beam search for slightly better results
            length_penalty=1.0,
            early_stopping=True,
            no_repeat_ngram_size=2  # Avoid repeating phrases
        )
    
    # Decode the tokenized output to readable text
    description = processor.decode(outputs[0], skip_special_tokens=True)
    return description  # Return the caption as string

# This function is the external entry point for screen capture
def start_capture(monitor_index):
    """
    Initiates screen capture on a specific monitor index.
    """
    global selected_monitor_index
    selected_monitor_index = monitor_index  # Set global index to chosen monitor
    return capture_and_describe_once()  # Trigger a one-time capture and description

# Function that performs a single screen capture and description
def capture_and_describe_once():
    global selected_monitor_index
    print("Starting single screen capture...")  # Log for debug
    
    with mss.mss() as sct:  # Start screen capture context
        monitor = sct.monitors[selected_monitor_index]  # Access monitor by index

        print(f"Capturing monitor {selected_monitor_index}")  # Debug print
        screenshot = sct.grab(monitor)  # Capture screenshot of selected monitor

        # Convert raw screenshot data to a proper RGB image for processing
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        # Use BLIP model to describe the captured screen image
        description = get_image_description(img)

        print(f"Description: {description}")  # Print generated description
        return description  # Return the caption for use elsewhere

# Optional GUI function to manually select a monitor using a dropdown
def select_monitor_popup():
    def on_select(event):
        # On dropdown selection, update the global monitor index (note: MSS starts from 1)
        global selected_monitor_index
        selected_monitor_index = monitor_combobox.current() + 1
        print(f"Monitor {selected_monitor_index} selected.")  # Confirmation log
        root.destroy()  # Close the selection popup

    # Initialize the Tkinter root window
    root = tk.Tk()
    root.title("Select Monitor")  # Set window title

    # Instruction label
    label = tk.Label(root, text="Select Monitor:")
    label.pack(pady=5)

    # List available monitors (skip index 0 which represents all monitors)
    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # Exclude 0 (full screen capture)
        monitor_names = [f"Monitor {i+1}" for i in range(len(monitors))]  # Friendly names

    # Create a Combobox dropdown with monitor options
    monitor_combobox = ttk.Combobox(root, values=monitor_names)
    monitor_combobox.current(0)  # Set default selection to first monitor
    monitor_combobox.bind("<<ComboboxSelected>>", on_select)  # Bind selection event
    monitor_combobox.pack(pady=10)

    root.mainloop()  # Launch the popup loop
    print("Monitor selection completed.")  # Confirmation log

# If this file is run as a standalone script, allow manual monitor selection and run capture
if __name__ == "__main__":
    select_monitor_popup()  # Show GUI to pick a monitor
    start_capture(selected_monitor_index)  # Capture and describe selected monitor
