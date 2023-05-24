import webbrowser
import keyboard
import pyautogui
import pyperclip
import win32gui
import win32con

previous_text = ""

def show_message_box():
    global previous_text
    # copy the highlighted text
    pyautogui.hotkey('ctrl', 'c')    
    current_text = pyperclip.paste()

    if current_text != previous_text:
        # message box
        win32gui.MessageBox(
            None,
            current_text,
            "InstantGPT says:",
            win32con.MB_OK | win32con.MB_SETFOREGROUND
        )
    else: 
        # open ChatGPT for convenience
        webbrowser.open('https://chat.openai.com')
        
    previous_text = current_text
    
previous_text = pyperclip.paste()

keyboard.add_hotkey("ctrl+shift+o", show_message_box)
keyboard.wait('esc')
# watch Date A Live