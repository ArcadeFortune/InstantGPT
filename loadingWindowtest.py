import tkinter as tk
import keyboard

    
def instantGPT():
    print('test')
    global loadingWindow
    loadingWindow.destroy()

# Create a window
def new_func():
    global loadingWindow
    loadingWindow = tk.Tk()
    

# Call the loadWindow function
    # Set the window settings
    loadingWindow.title("Self-Closing Window")
    # Remove the buttons on top
    loadingWindow.overrideredirect(True)
    # Move the window to the current mouse position
    loadingWindow.geometry(f"+{loadingWindow.winfo_pointerx()}+{loadingWindow.winfo_pointery()}")
    # Write text into the window
    content_label = tk.Label(loadingWindow, text="Loading...", font=("Arial", 22))
    content_label.pack()
    
    # Do something while loading the window
    loadingWindow.after(1000, instantGPT)

# Start the Tkinter event loop
    loadingWindow.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# new_func()
keyboard.add_hotkey("ctrl+shift+o", new_func)
keyboard.wait('esc')

