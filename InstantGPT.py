import webbrowser
import keyboard
import pyautogui
import pyperclip
import win32gui
import win32con
import os
from dotenv import load_dotenv
import openai
import tkinter as tk

load_dotenv()

root = tk.Tk()
label = tk.Label(root, font=("Arial", 20))
label.pack()

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
            answer = sendRequest(current_text)

            # Show message box
            label.config(text=answer)
        else:
            # No highlighted text, open OpenAI website
            webbrowser.open('https://chat.openai.com')
            
        
    previous_text = current_text

def sendRequest(current_text):
    answer = ""
            
    message=[{"role": "user", "content": current_text}]
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
            )
    answer = response['choices'][0]['message']['content']
    return answer
    
previous_text = pyperclip.paste()

keyboard.add_hotkey("ctrl+shift+o", show_message_box)
root.mainloop()
keyboard.wait('esc')
# watch Date A Live