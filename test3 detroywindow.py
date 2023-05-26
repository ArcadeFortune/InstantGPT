import win32gui
import win32con
import time
import threading
import tkinter as tk

answer = 'test'



# Create a window 
loadingWindow = tk.Tk()

# Set the window settings
loadingWindow.title("Self-Closing Window")
# Remove the buttons ontop
loadingWindow.overrideredirect(True)
# Move the window to the current mouse position
loadingWindow.geometry(f"+{loadingWindow.winfo_pointerx()}+{loadingWindow.winfo_pointery()}")
# Write text into the window
content_label = tk.Label(loadingWindow, text="Loading...", font=("Arial", 22))
content_label.pack()
# idk
# content_label.config(text=response.text)
# window.geometry(f"{content_label.winfo_reqwidth()}x{content_label.winfo_reqheight()}")

# Function to close the window after 2 seconds
def sendRequest():
  #call
    loadingWindow.destroy()

# Do something while loading the window
loadingWindow.after(1000, sendRequest)
loadingWindow.mainloop()

