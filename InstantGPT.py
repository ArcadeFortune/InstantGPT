import os
import openai
import keyboard
import pyautogui
import pyperclip
import threading
import webbrowser
import tkinter as tk
from dotenv import load_dotenv
from markdown2 import Markdown
from tkinterweb import HtmlFrame

# OpenAI API key
load_dotenv()
key = os.getenv('key')
openai.api_key = key

# Markdown
markdowner = Markdown()

# Global variables
previous_text = pyperclip.paste()
received = False

def instantGPT():
  global previous_text
  global received
  current_text = readHighlightedText()
  
  root = tk.Tk()
  
  if current_text: # Error handling
    if current_text != previous_text:
      answer = sendRequest(current_text)
      if answer:          
        received = True # Confirm that answer has been received
        converted = markdowner.convert(answer)
        myhtmlframe = HtmlFrame(root, horizontal_scrollbar="auto", messages_enabled=False)
        # myhtmlframe.messages_enabled = False
        myhtmlframe.load_html(converted)
        myhtmlframe.pack(fill="both", expand=True)
        root.mainloop()
        
      else:
        print("Something went wrong with the API request")
        
    else:
      # No highlighted text, open OpenAI website
      print("No highlighted text, open OpenAI website")
      webbrowser.open('https://chat.openai.com')
      
  else: # Error handling
    print("Something went wrong with the highlighted text")
    
  previous_text = current_text # Update previous text

def readHighlightedText():
  pyautogui.hotkey('ctrl', 'c')    
  current_text = pyperclip.paste()
  print("highlighted text: " + current_text)
  return current_text

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

def loadLoadingWindow():
  global received
  global loadingWindow
  global content_label  
  received = False
  
  loadingWindow = tk.Tk()
  loadingWindow.title("Self-Closing Window") # Title  
  loadingWindow.overrideredirect(True) # No buttons on top row  
  loadingWindow.geometry(f"+{loadingWindow.winfo_pointerx()}+{loadingWindow.winfo_pointery()}") # Move window to current mouse position
  loadingWindow.attributes("-topmost", True) # Appear on top
  
  content_label = tk.Label(loadingWindow, text="Loading...", font=("Arial", 22)) # Text
  content_label.pack() # Necessary
  
  loadingWindow.after(10, load_loading_window) # Infinite loop
  loadingWindow.mainloop() # Run window

def load_loading_window():
  global received
  global content_label
  loading_texts = ["Loading.", "Loading..", "Loading..."]
  index = 0

  def update_content():
    nonlocal index
    if not received:
      content_label.config(text=loading_texts[index])
      index = (index + 1) % len(loading_texts)
      loadingWindow.after(500, update_content)
    else:
      loadingWindow.destroy()


  update_content()

def startThreads():
  print('starting threads...')
  # thread1 = threading.Thread(target=loadLoadingWindow)
  thread2 = threading.Thread(target=instantGPT)

  # thread1.start()
  thread2.start()

keyboard.add_hotkey("ctrl+shift+o", startThreads)
keyboard.wait('esc')

# watch Date A Live