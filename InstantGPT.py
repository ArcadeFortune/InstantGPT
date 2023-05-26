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
from markdown2 import Markdown
from tkinterweb import HtmlFrame
markdowner = Markdown()
loadingWindow = tk.Tk()

load_dotenv()

key = os.getenv('key')
openai.api_key = key
previous_text = ""


def instantGPT():
    global previous_text
    current_text = readHighlightedText(previous_text)
    root = tk.Tk()
    


    if current_text: # Error handling
        if current_text != previous_text:
            
            
            
            print("sending request...", end="\r")
            answer = sendRequest(current_text)
            print("answer: " + answer)
            converted = markdowner.convert(answer)
            myhtmlframe = HtmlFrame(root, horizontal_scrollbar="auto")
            myhtmlframe.load_html(converted)
            myhtmlframe.pack(fill="both", expand=True)

            root.mainloop()
            # win32gui.PostMessage(message, win32con.WM_CLOSE, 0, 0)
        else:
            # No highlighted text, open OpenAI website
            print("No highlighted text, open OpenAI website")
            webbrowser.open('https://chat.openai.com')
            
    else: # Error handling
        win32gui.MessageBox(0, "Something went wrong with your highlighted text...", "Instant GPT", win32con.MB_OK | win32con.MB_SETFOREGROUND)
        
    previous_text = current_text
    # global loadingWindow
    # loadingWindow.destroy()


def readHighlightedText(previous_text):
    pyautogui.hotkey('ctrl', 'c')    
    current_text = pyperclip.paste()
    print("highlighted text: " + current_text)
    return current_text

def sendRequest(current_text):
    answer = ""
            
    message=[{"role": "user", "content": current_text}]
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
            )
    answer = response['choices'][0]['message']['content']
    return answer
    
def loadWindow():
    print('loading window...')
    # Create a window 
    global loadingWindow
    # Set the window settings
    loadingWindow.title("Self-Closing Window")
    # Remove the buttons ontop
    loadingWindow.overrideredirect(True)
    # Move the window to the current mouse position
    loadingWindow.geometry(f"+{loadingWindow.winfo_pointerx()}+{loadingWindow.winfo_pointery()}")
    # Write text into the window
    content_label = tk.Label(loadingWindow, text="Loading...", font=("Arial", 22))
    content_label.pack()
    

    # Do something while loading the window
    loadingWindow.after(1, instantGPT)
    loadingWindow.mainloop()

# Listen for hotkey
previous_text = pyperclip.paste()
keyboard.add_hotkey("ctrl+shift+o", instantGPT)
keyboard.wait('esc')
# watch Date A Live