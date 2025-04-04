from typing import Any
import os
import subprocess
import webbrowser
import base64
import threading

import speech_recognition as sr
import pywhatkit as kit
import pyautogui
import keyboard
import streamlit as st
import google.generativeai as genai
import pyttsx3
import pyjokes

# Initialize speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure Gemini API (ensure you use a secure method for your API key)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDZ6yDuQgQWxzc5Qq24Dpf_BkvcOjx_SP8")
genai.configure(api_key=GOOGLE_API_KEY)
geminiModel = genai.GenerativeModel("gemini-1.5-pro")
chat = geminiModel.start_chat(history=[])

def get_gemini_response(query: str) -> str:
    try:
        instantResponse = chat.send_message(query, stream=True)
        response_text = ' '.join(
            [outputChunk.text for outputChunk in instantResponse if hasattr(outputChunk, 'text')]
        )
        return response_text
    except AttributeError as e:
        st.error(f"Error in Gemini API response: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
    return ""

def speak(text: str) -> None:
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech).start()

def image_to_base64(image_path: str) -> Any:
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image file '{image_path}' not found.")
        return None

# Sidebar and UI styling
st.sidebar.title('Help Menu')
st.sidebar.write('This is JARVIS, your personal assistant. Here are some ways to use it:')
st.sidebar.markdown("""
- **Open Application**: Type an app name to open it.
- **Open Website**: Enter a URL to open a website.
- **Chat**: Ask JARVIS anything!
- **Tell Joke**: Hear a joke to lighten the mood.
- **Text-to-Speech**: Convert your text to speech output.
""")

st.sidebar.title('Features Menu')
st.sidebar.write('JARVIS offers the following features:')
st.sidebar.markdown("""
- Application Launcher  
- Website Launcher  
- Joke Teller  
- Text-to-Speech Converter
""")

# Load images (adjust file paths as needed)
background_image_path = os.path.join(os.path.dirname(__file__), "jarvis.png")
logo_image_path = os.path.join(os.path.dirname(__file__), "jarvis1.jpg")
background_image_base64 = image_to_base64(background_image_path)
logo_image_base64 = image_to_base64(logo_image_path)

if background_image_base64:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{background_image_base64}");
            background-size: cover;
            background-position: center;
            color: #FFFFFF;
            font-family: 'Arial', sans-serif;
        }}
        .stButton > button {{
            background-color: #ff6f91;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            transition: all 0.2s ease-in-out;
        }}
        .stButton > button:hover {{
            background-color: #ff4d7e;
        }}
        .stSidebar {{
            background: #020024;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if logo_image_base64:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpg;base64,{logo_image_base64}" alt="JARVIS Logo" style="width: 200px;">
        </div>
        """,
        unsafe_allow_html=True
    )

st.title('JARVIS - Your Personal Assistant')

# Maintain chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Dictionary for launching common desktop applications
universal_app_names = {
    'word': 'winword.exe',
    'excel': 'excel.exe',
    'powerpoint': 'powerpnt.exe',
    'chrome': 'chrome.exe',
    'notepad': 'notepad.exe',
    'vscode': 'code.exe',
    'paint': 'mspaint.exe',
    'outlook': 'outlook.exe',
    'edge': 'msedge.exe',
    'calculator': 'calc.exe',
    'command prompt': 'cmd.exe',
    'control panel': 'control.exe',
    'file explorer': 'explorer.exe',
    'onenote': 'onenote.exe',
    'teams': 'teams.exe',
    'skype': 'skype.exe',
    'pycharm': 'pycharm64.exe',
    'android studio': 'studio64.exe',
    'virtualbox': 'VirtualBox.exe',
    '7zip': '7zFM.exe',
    'winrar': 'winrar.exe',
    'task manager': 'taskmgr.exe',
    'windows media player': 'wmplayer.exe',
    'microsoft store': 'WinStore.App.exe',
    'visual studio': 'devenv.exe',
    'invision studio': 'InVisionStudio.exe',
    'android emulator': 'emulator.exe',
    'photos': 'microsoft.photos.exe',
    'xbox game bar': 'gamebar.exe',
    'wsl': 'wsl.exe',
    'firewall': 'firewall.cpl',
    'windows defender': 'msmpeng.exe',
    'camera': 'camera.exe',
    'calendar': 'wlcalendar.exe',
    'paint 3d': 'paint3d.exe',
    'wordpad': 'wordpad.exe',
    'snipping tool': 'SnippingTool.exe',
    'microsoft whiteboard': 'Whiteboard.exe',
    'google drive': 'googledrivesync.exe',
    'onedrive': 'OneDrive.exe',
    'powershell': 'powershell.exe',
    'settings': 'SystemSettings.exe',
}

def open_application(app_name: str):
    app_path = universal_app_names.get(app_name.lower())
    if app_path:
        try:
            os.startfile(app_path)
            speak(f"Opening {app_name}")
        except Exception as e:
            st.error(f"Error opening {app_name}: {str(e)}")
    else:
        st.error(f"Application '{app_name}' not found.")

def open_website(url: str):
    try:
        if not url.startswith("http"):
            url = f"https://{url}.com"
        webbrowser.open(url)
        st.write(f"Opening website: {url}")
        speak(f"Opening website {url}")
    except Exception as e:
        st.error(f"Error opening website {url}: {str(e)}")

def take_voice_command() -> Any:
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            st.info("Listening...")
            audio = recognizer.listen(source, timeout=5)
            st.info("Recognizing...")
            command = recognizer.recognize_google(audio)
            st.write(f"User said: {command}")
            return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that. Please repeat.")
    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the service.")
    except Exception as e:
        speak(f"An error occurred: {str(e)}")
    return None

# Main UI options
option = st.selectbox('Select an Option:', [
    'Open Application',
    'Open Website',
    'Chat',
    'Tell Joke',
    'Text-to-Speech',
    'Voice Command'
])

if option == 'Open Application':
    app_name = st.text_input('Enter Application Name:')
    if st.button('Open Application'):
        open_application(app_name)

elif option == 'Open Website':
    url = st.text_input('Enter Website URL:')
    if st.button('Open Website'):
        open_website(url)

elif option == 'Chat':
    user_message = st.text_input('Enter your message:')
    if st.button('Send'):
        response = get_gemini_response(user_message)
        if response:
            st.write("**JARVIS:** " + response)
            st.session_state.chat_history.append(('User', user_message))
            st.session_state.chat_history.append(('JARVIS', response))

elif option == 'Tell Joke':
    joke = pyjokes.get_joke()
    st.write("**JARVIS:** " + joke)
    speak(joke)

elif option == 'Text-to-Speech':
    text = st.text_area('Enter text to convert to speech:')
    if st.button('Convert to Speech'):
        engine.say(text)
        engine.runAndWait()
        st.write("**JARVIS:** " + text)

elif option == 'Voice Command':
    st.write("Click the button and speak your command (local microphone required).")
    if st.button("Start Voice Command"):
        command = take_voice_command()
        if command:
            st.write("Recognized Command: " + command)
            # Here you can add logic to process the voice command (e.g., open application, website, etc.)
            if "open" in command:
                if "website" in command:
                    site = command.replace("open website", "").strip()
                    open_website(site)
                else:
                    app = command.replace("open", "").strip()
                    open_application(app)
            elif "close" in command:
                st.write("Close command received (functionality can be added).")
            elif "play music" in command:
                song = command.replace("play music", "").strip()
                try:
                    kit.playonyt(song)
                    speak(f"Playing {song} on YouTube.")
                except Exception as e:
                    speak(f"Error playing music: {str(e)}")
            # Add further command handling as needed

# Footer or extra UI elements can be added below
st.write("JARVIS is ready at your service!")

