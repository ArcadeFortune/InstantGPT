import os
import keyboard
import pyautogui
import pyperclip
import threading
import webbrowser
import openai
import tkinter as tk
from dotenv import load_dotenv
from markdown2 import Markdown
from tkinterweb import HtmlFrame

# OpenAI API key
load_dotenv()
key = os.getenv('key')
openai.api_key = key

markdowner = Markdown()
text = 'eiusmod tempor incididunt ut labolaborum.'

# Global variables
previous_text = pyperclip.paste()
received = False
highlighted = True

def beautifyLoadingWindow():
  global myhtmlframe
  global root
  global content_label
  root = tk.Tk()
  root.overrideredirect(True) # No buttons on top row  
  root.title("InstantGPT")
  root.geometry(f"+{root.winfo_pointerx()}+{root.winfo_pointery()}") # Move window to current mouse position
  root.attributes("-topmost", True) # Appear on top
  content_label = tk.Label(root, text="Loading...", font=("Arial", 22)) # Text
  content_label.pack() # Necessary
  
  converted = markdowner.convert("# Loading...")
  myhtmlframe = HtmlFrame(root, horizontal_scrollbar="auto", messages_enabled=False)
  # myhtmlframe.load_html(converted)
  # myhtmlframe.pack(fill="both", expand=True)
  
def InstantGPT():  
  global previous_text
  global received
  current_text = readHighlightedText()
  
  if current_text: # Error handling
    if current_text != previous_text:      
      answer = sendRequest(current_text)
      if answer:
        global myhtmlframe
        global root
        global content_label
        content_label.pack_forget()
        root.overrideredirect(False) # Buttons on top row  
        converted = markdowner.convert(answer)
        myhtmlframe.load_html(converted)  
        myhtmlframe.pack(fill="both", expand=True)
                
        resizeWindow()
      else:
        print("Something went wrong with the API request")
        
    else:
      # No highlighted text, open OpenAI website
      global highlighted
      highlighted = False
      print("No highlighted text, open OpenAI website")
      webbrowser.open('https://chat.openai.com')
      
  else: # Error handling
    print("Something went wrong with the highlighted text")
  
def sendRequest(current_text):  
  try:      
    answer = ""    
    print("sending request...", end="\r")
            
    message=[{"role": "user", "content": current_text}]
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message,
    )
    answer = response['choices'][0]['message']['content']
    print("returned answer: " + answer)
    return answer

  except openai.error.APIError as e:
    # Handle API errors
    return 'API Error:', str(e)

  except Exception as e:
    # Handle other exceptions
    return 'Error:', str(e)

def resizeWindow():
    frame_width = myhtmlframe.winfo_reqwidth()
    frame_height = myhtmlframe.winfo_reqheight()
    root.geometry(f"{frame_width}x{frame_height}")
    
def readHighlightedText():
  pyautogui.hotkey('ctrl', 'c')    
  current_text = pyperclip.paste()
  print("highlighted text: " + current_text)
  return current_text
      
def main():
  global root
  beautifyLoadingWindow()
  root.after(50, InstantGPT)
  root.after(100, readHighlightedText)
  root.mainloop()

keyboard.add_hotkey('ctrl+shift+o', main)
keyboard.wait('esc')