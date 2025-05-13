# Streamer AI Chatbot

## Overview
The Streamer AI Chatbot is a real-time, AI-powered chat system designed specifically for small streamers. This chatbot enhances audience engagement by generating dynamic, context-aware chat responses based on multiple real-time input sources, including:
- **Microphone Input**: Captures spoken words from the streamer.
- **Screen Capture**: Analyzes on-screen content to provide relevant responses.
- **Desktop Audio**: Listens to game sounds, music, or other desktop audio.

Unlike traditional bots that rely on static keyword-based triggers, this system integrates with OpenAI’s ChatGPT API (GPT-3.5 Turbo) to produce interactive and engaging responses. It mimics the chat culture of platforms like Twitch by incorporating randomly generated usernames, chat colors, and popular slang such as "PogChamp" or "KEKW."

This chatbot is built with Python and uses a **tkinter** GUI, allowing streamers to easily configure settings such as API credentials, input methods, and response timing. 

## Features
- **Multi-Input Processing**: Supports real-time input from microphone, screen capture, and desktop audio.
- **AI-Generated Responses**: Uses OpenAI's ChatGPT API to produce engaging, varied chat messages.
- **Custom Twitch-Style Chat Formatting**: Randomized usernames, colors, and meme-like responses.
- **User-Friendly GUI**: Built with `tkinter`, allowing easy configuration and customization.
- **Adjustable Timers**: Streamers can set timers for interaction frequency.
- **Automated Processing Loop**: Continuously gathers inputs and generates responses without manual intervention.
- **Error Handling & Notifications**: Warnings for missing configurations, invalid API keys, or capture errors.
- **Standalone Executable Support**: Can be compiled into a `.exe` for portability.

## Installation
### Requirements
To run this chatbot, ensure you have **Python 3.10** installed. Other versions may work but could have compatibility issues.

### Installing Dependencies
Run the following command to install all required dependencies:
```bash
pip install tk mss pillow torch transformers speechrecognition pyaudio requests openai numpy
```

### Additional Setup
#### **VB Audio Virtual Cable for Desktop Audio Input**
For capturing desktop/game audio, install **VB-Audio Virtual Cable**:
1. Download VB-Audio Virtual Cable from [here](https://vb-audio.com/Cable/).
2. Extract and install the software (`VBCABLE_Setup_x64.exe` for 64-bit systems).
3. Restart your computer.
4. Open Sound Settings:
   - **Output Device**: Set your speakers/headphones as usual.
   - **Recording Device**: Set `CABLE Output (VB-Audio Virtual Cable)` as the default recording device.
   - **Application-Specific Routing**: Route specific apps (e.g., games, music) to `CABLE Input` for better control.


### How to get the mic to be compatible with the program
You need to set the application to format the mic input to be picked up by more then one program at once. This is done by going to... 
1. Control Panel > 
2. Sound > 
3. Recording > 
4. Right click desired device 
5. Choose "Properties" from drop down menu. 
6. Click the "advanced" tab 
7. Turn off the options for "allow applications to take exclusive control of this device" 
AND 
8. "give exclusive mode applications priority". 
(This is what you do for you main mic btw)

## Usage
### Running the Program
1. **Launch the chatbot GUI** by running:
   ```bash
   python Merged_V7.py
   ```
2. **Enter your ChatGPT API Key**: Obtain one from [OpenAI](https://openai.com/) and enter it in the GUI.
3. **Choose Your Input Methods**:
   - Enable **Microphone Input** to capture speech.
   - Enable **Screen Capture** (select a monitor if necessary).
   - Enable **Desktop Audio** for transcribing background sounds.
4. **Adjust Chat Settings**:
   - Set response timers (e.g., 10s reset, 5s listening duration).
   - Configure additional behavior (e.g., background info, topics).
5. **Click "Start Program"**: The chatbot will begin generating responses based on real-time inputs.

## Building an Executable
If you want to create a standalone `.exe` version, run:
```bash
pyinstaller --console --onefile --add-data "Screen_Desc.py;." --add-data "Get_Mic_Input.py;." --add-data "pyaudio_desktop.py;." Merged_V7.py
```
This generates an executable file that can be run without needing Python installed.

## API Key Setup
1. **Create an OpenAI Account** at [OpenAI](https://openai.com/).
2. **Generate an API Key**:
   - Go to the "API Keys" section.
   - Click **"Create new secret key"**.
   - Store the key securely (it won’t be shown again).
3. **Token Usage & Costs**:
   - OpenAI charges per token used.
   - Monitor usage in your OpenAI dashboard.
   - Set up billing restrictions if needed.

## Customization
### Command Prompt Colors
To change the command prompt color scheme:
1. Open **Command Prompt** (`cmd`).
2. Click the **title bar** → **Properties**.
3. Go to **Colors** → Customize text/background colors.
4. Click **OK**, then restart the program.

### Modify Chat Behavior
- Change Twitch-style chat frequency by modifying response generation probabilities.
- Adjust the API prompt for different response styles.
- Customize usernames, chat slang, and randomness levels.

## Troubleshooting
### Audio Issues
- **Microphone Not Detected**: Check input device settings.
- **Desktop Audio Not Capturing**: Ensure VB-Cable is correctly set up.

### ChatGPT API Errors
- **Invalid API Key**: Double-check your key in OpenAI’s API section.
- **Rate Limit Exceeded**: Reduce the frequency of API calls.
- **No Response from ChatGPT**: OpenAI servers may be down; try again later.

## Future Improvements
- **Support for More AI Models**: Integration with GPT-4 or fine-tuned models.
- **More Input Sources**: Webcam-based emotion detection, live transcription.
- **Stream Overlay Support**: Display AI-generated chat messages in an overlay.

## License
This project is **open-source**. Modify and redistribute freely, but please credit the original creator.


## GUI (Once program is running)
- **ChatGPT API key, this is needed to actully get a response from the chatgpt api server, this program is using gpt 3.5 turbo for cost reasons
- **Streamer username is the custom username from the user, and is how the program refers to the user
- **Enable Chatgpt box is toggle clickable on or off and activates the option, giving a response from chatgpt
- **Enable Mic input box is toggle clickable on or off and activates the option, Collecting the data from the mic
- **Enable Screen input box is toggle clickable on or off and activates the option, Collecting the data from the BLIP API and gets a description of what is seen on the screen. If activated, the screen can be selected from the bottom
- **Enable Desktop audio input box is toggle clickable on or off and activates the option, Collecting the data from the Desktop using VB Cable Application
- **Enable background info is toggleable and if selected, you can type background info into the text box, which helps the ai structure the messages
- **Enable Main topics and Behavior is toggleable and if selected, you can type How you want the program to act into the text box, which helps the ai structure the messages again
- **Reset time is how long the program takes to restart the loop (Of collecting the selected data and creating messages)
- **Audio duration is how long the desktop audio setting listens for, before turning into text and submitting the data to format the messages in respeonse, you have to use the VB audio cable to do this