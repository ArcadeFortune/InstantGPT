import webbrowser
import keyboard
import pyautogui
import pyperclip
import win32gui
import win32con
import os
from dotenv import load_dotenv
import openai

load_dotenv()

key = os.getenv('key')
openai.api_key = key


def show_message_box():
    previous_text = ""
    # copy the highlighted text
    pyautogui.hotkey('ctrl', 'c')    
    current_text = pyperclip.paste()

    

    if current_text:
        # There is highlighted text
        if current_text != previous_text:
            answer = ""
            
            message=[{"role": "user", "content": current_text}]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
            )
            answer = response['choices'][0]['message']['content']

            # Show message box
            win32gui.MessageBox(
                None,
                answer,
                "InstantGPT says:",
                win32con.MB_OK | win32con.MB_SETFOREGROUND
            )
        else:
            # No highlighted text, open OpenAI website
            webbrowser.open('https://chat.openai.com')
            
        
    previous_text = current_text
    
previous_text = pyperclip.paste()

keyboard.add_hotkey("ctrl+shift+o", show_message_box)
keyboard.wait('esc')
# watch Date A Live