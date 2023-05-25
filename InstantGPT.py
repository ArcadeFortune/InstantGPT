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

previous_text = ""

def show_message_box():
    global previous_text
    # copy the highlighted text
    pyautogui.hotkey('ctrl', 'c')    
    current_text = pyperclip.paste()
    message=[{"role": "user", "content": current_text}]
    response = openai.Completion.create(
        model="gpt-4",
        max_tokens=150,
        temperature=0.9,
        messages=message,
    )
    
    print (response)
    

    if current_text:
        # There is highlighted text
        if current_text != previous_text:
            # Show message box
            win32gui.MessageBox(
                None,
                current_text,
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