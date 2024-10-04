import os
import streamlit as st
import google.generativeai as genai
import pyttsx3
import pyjokes
import base64
import webbrowser

engine = pyttsx3.init()

GOOGLE_API_KEY = "AIzaSyDZ6yDuQgQWxzc5Qq24Dpf_BkvcOjx_SP8"
genai.configure(api_key=GOOGLE_API_KEY)

geminiModel = genai.GenerativeModel("gemini-pro")
chat = geminiModel.start_chat(history=[])

def get_gemini_response(query):
    try:
        instantResponse = chat.send_message(query, stream=True)
        response_text = ' '.join([outputChunk.text for outputChunk in instantResponse if hasattr(outputChunk, 'text')])
        return response_text
    except AttributeError as e:
        st.error(f"Error in Gemini API response: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")

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

background_image_path = os.path.join(os.path.dirname(__file__), "jarvis.png")
logo_image_path = os.path.join(os.path.dirname(__file__), "jarvis1.jpg")

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"Image file '{image_path}' not found.")
        return None

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
        h1, h2, h3, h4, h5, h6, p {{
            color: white;
        }}
        .stButton > button:hover {{
            background-color: #ff4d7e;
        }}
        .stSidebar {{
            background: #020024;
            color: white;
        }}
        .chatbox {{
            border: 2px solid #ff6f91;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            background-color: #f8f9fa;
            max-height: 300px;
            overflow-y: scroll;
        }}
        .user-msg {{
            text-align: right;
            color: #007bff;
            margin-bottom: 5px;
        }}
        .jarvis-msg {{
            text-align: left;
            color: #28a745;
            margin-bottom: 5px;
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

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

universal_app_names = {
    'word': 'winword.exe',
    'excel': 'excel.exe',
    'powerpoint': 'powerpnt.exe',
    'chrome': 'chrome.exe',
    'notepad': 'notepad.exe',
    'vscode': 'code.exe',
    'paint': 'mspaint.exe',
    'outlook': 'outlook.exe',
    'firefox': 'firefox.exe',
    'edge': 'msedge.exe',
    'calculator': 'calc.exe',
    'command prompt': 'cmd.exe',
    'control panel': 'control.exe',
    'file explorer': 'explorer.exe',
    'onenote': 'onenote.exe',
    'teams': 'teams.exe',
    'skype': 'skype.exe',
    'spotify': 'spotify.exe',
    'steam': 'steam.exe',
    'slack': 'slack.exe',
    'discord': 'discord.exe',
    'zoom': 'zoom.exe',
    'vlc': 'vlc.exe',
    'acrobat': 'acrord32.exe',
    'photoshop': 'photoshop.exe',
    'illustrator': 'illustrator.exe',
    'premiere': 'premiere.exe',
    'after effects': 'afterfx.exe',
    'audition': 'audition.exe',
    'notepad++': 'notepad++.exe',
    'sublime text': 'sublime_text.exe',
    'pycharm': 'pycharm64.exe',
    'intellij idea': 'idea64.exe',
    'android studio': 'studio64.exe',
    'eclipse': 'eclipse.exe',
    'putty': 'putty.exe',
    'mysql workbench': 'mysqlworkbench.exe',
    'xampp': 'xampp-control.exe',
    'postman': 'Postman.exe',
    'github desktop': 'github.exe',
    'docker': 'Docker Desktop.exe',
    'virtualbox': 'VirtualBox.exe',
    'vmware': 'vmware.exe',
    'gimp': 'gimp-2.10.exe',
    'audacity': 'audacity.exe',
    'blender': 'blender.exe',
    'kodi': 'kodi.exe',
    'obs studio': 'obs64.exe',
    'cyberduck': 'cyberduck.exe',
    'filezilla': 'filezilla.exe',
    'rstudio': 'rstudio.exe',
    'jupyter notebook': 'jupyter-notebook.exe',
    'jupyter lab': 'jupyter-lab.exe',
    'safari': 'safari.exe',
    'opera': 'opera.exe',
    'opera gx': 'opera_gx.exe',
    '7zip': '7zFM.exe',
    'winrar': 'winrar.exe',
    'task manager': 'taskmgr.exe',
    'itunes': 'itunes.exe',
    'movie maker': 'moviemk.exe',
    'windows media player': 'wmplayer.exe',
    'groove music': 'groove.exe',
    'microsoft store': 'WinStore.App.exe',
    'visual studio': 'devenv.exe',
    'netbeans': 'netbeans.exe',
    'brackets': 'brackets.exe',
    'atom': 'atom.exe',
    'xcode': 'xcode.exe',
    'lightroom': 'lightroom.exe',
    'invision studio': 'InVisionStudio.exe',
    'figma': 'figma.exe',
    'sketchup': 'SketchUp.exe',
    'postgreSQL': 'pgAdmin4.exe',
    'dbeaver': 'dbeaver.exe',
    'heidisql': 'heidisql.exe',
    'soapUI': 'SoapUI-5.5.0.exe',
    'wireshark': 'Wireshark.exe',
    'android emulator': 'emulator.exe',
    'vivaldi': 'vivaldi.exe',
    'photos': 'microsoft.photos.exe',
    'your phone': 'yourphone.exe',
    'solitaire': 'solitaire.exe',
    'xbox game bar': 'gamebar.exe',
    'microsoft edge dev': 'msedge_dev.exe',
    'fiddler': 'fiddler.exe',
    'free download manager': 'fdm.exe',
    'handbrake': 'HandBrake.exe',
    'obsidian': 'obsidian.exe',
    'terraform': 'terraform.exe',
    'bitwarden': 'bitwarden.exe',
    'lastpass': 'lastpass.exe',
    'keepass': 'keepass.exe',
    'teamviewer': 'TeamViewer.exe',
    'anydesk': 'AnyDesk.exe',
    'skype for business': 'lync.exe',
    'zoom rooms': 'ZoomRooms.exe',
    'libreoffice writer': 'soffice.exe',
    'libreoffice calc': 'scalc.exe',
    'libreoffice impress': 'simpress.exe',
    'apache directory studio': 'ApacheDirectoryStudio.exe',
    'dbvisualizer': 'dbvis.exe',
    'pandoc': 'pandoc.exe',
    'wsl': 'wsl.exe',
    'firewall': 'firewall.cpl',
    'windows defender': 'msmpeng.exe',
    'camera': 'camera.exe',
    'alarm': 'alarmclock.exe',
    'calendar': 'wlcalendar.exe',
    'map': 'mapcontrol.exe',
    'news': 'msnews.exe',
    'weather': 'weather.exe',
    'microsoft edge canary': 'msedge_canary.exe',
    'paint 3d': 'paint3d.exe',
    'wordpad': 'wordpad.exe',
    'snipping tool': 'SnippingTool.exe',
    'microsoft whiteboard': 'Whiteboard.exe',
    'google drive': 'googledrivesync.exe',
    'dropbox': 'Dropbox.exe',
    'onedrive': 'OneDrive.exe',
    'box drive': 'Box.exe',
    'zoom player': 'ZoomPlayer.exe',
    'powerdvd': 'PowerDVD.exe',
    'twitch': 'Twitch.exe',
    'opera developer': 'OperaDev.exe',
    'vivaldi snapshot': 'VivaldiSnapshot.exe',
    'nitro pdf': 'NitroPDF.exe',
    'mirc': 'mirc.exe',
    'tortoisegit': 'TortoiseGitProc.exe',
    'gitkraken': 'GitKraken.exe',
    'powershell': 'powershell.exe',
    'xmind': 'xmind.exe',
    'mindmanager': 'MindManager.exe',
    'draw.io': 'draw.io.exe',
    'tweaks': 'tweakui.exe',
    'power automate': 'PowerAutomate.exe',
    'onenote 2016': 'ONENOTE.exe',
    'visual studio code insiders': 'code-insiders.exe',
    'microsoft access': 'msaccess.exe',
    'microsoft publisher': 'MSPUB.exe',
    'adobe acrobat': 'Acrobat.exe',
    'coreldraw': 'CorelDRW.exe',
    'wacom tablet': 'WacomTablet.exe',
    'quicken': 'qw.exe',
    'quickbooks': 'qbw32.exe',
    'thunderbird': 'thunderbird.exe',
    'pandora': 'pandora.exe',
    'netflix': 'Netflix.exe',
    'prime video': 'PrimeVideo.exe',
    'hulu': 'hulu.exe',
    'discord canary': 'discordcanary.exe',
    'epic games launcher': 'EpicGamesLauncher.exe',
    'origin': 'Origin.exe',
    'battle.net': 'Battle.net.exe',
    'uplay': 'Uplay.exe',
    'gog galaxy': 'GOGGalaxy.exe',
    'rockstar games launcher': 'LauncherPatcher.exe',
    'epub reader': 'EpubReader.exe',
    'kindle': 'Kindle.exe',
    'calibre': 'calibre.exe',
    'stremio': 'Stremio.exe',
    'plex': 'Plex.exe',
    'sonarr': 'Sonarr.exe',
    'radarr': 'Radarr.exe',
    'jd-gui': 'jd-gui.exe',
    'minecraft launcher': 'MinecraftLauncher.exe',
    'bluestacks': 'BlueStacks.exe',
    'mame': 'mame.exe',
    'retroarch': 'retroarch.exe',
    'gog': 'GOGGalaxy.exe',
    'vrchat': 'VRChat.exe',
    'rec room': 'RecRoom.exe',
    'second life': 'SecondLife.exe',
    'steam vr': 'vrserver.exe',
    'origin games': 'Origin.exe',
    'rockstar launcher': 'LauncherPatcher.exe',
    'iTunes': 'iTunes.exe',
    'nox player': 'nox.exe',
    'memu': 'Memu.exe',
    'genymotion': 'genymotion.exe',
    'bluestacks 5': 'BlueStacks_5.exe',
    'oxford dictionary': 'OxfordDict.exe',
    'linguee': 'Linguee.exe',
    'translate': 'Translate.exe',
    'grammar check': 'Grammarly.exe',
    'quillbot': 'Quillbot.exe',
    'chatgpt': 'ChatGPT.exe',
    'microsoft edge beta': 'msedge_beta.exe',
    'slack beta': 'slack_beta.exe',
    'zoom beta': 'zoom_beta.exe',
    'teams beta': 'teams_beta.exe',
    'chrome beta': 'chrome_beta.exe',
    'firefox beta': 'firefox_beta.exe',
    'explorer beta': 'explorer_beta.exe',
    'movie maker beta': 'moviemk_beta.exe'
}

def open_application(app_name):
    app_path = universal_app_names.get(app_name.lower())
    if app_path:
        try:
            os.startfile(app_path)
        except Exception as e:
            st.error(f"Error opening {app_name}: {str(e)}")
    else:
        st.error(f"Application '{app_name}' not found.")

def open_website(url):
    try:
        webbrowser.open(f"{url}.com")
        st.write(f"Opening website: {url}")  # Simulate opening a website
    except Exception as e:
        st.error(f"Error opening website {url}: {str(e)}")

option = st.selectbox('Select an Option:', [
    'Open Application',
    'Open Website',
    'Chat',
    'Tell Joke',
    'Text-to-Speech'
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

elif option == 'Text-to-Speech':
    text = st.text_area('Enter text to convert to speech:')
    if st.button('Convert to Speech'):
        engine.say(text)
        engine.runAndWait()
        st.write("**JARVIS:** " + text)
