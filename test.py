import threading
import requests
import win32gui
import win32con
import openai
from dotenv import load_dotenv
import os

load_dotenv()


key = os.getenv('key')
openai.api_key = key

def sendRequest(current_text):
    answer = ""
            
    message=[{"role": "user", "content": current_text}]
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message,
            )
    answer = response['choices'][0]['message']['content']
    return answer
  
  
def send_request():
    try:
        # Send the request to the API
        answer = sendRequest("what can you do?")
        print("answer: ", answer)
        # Process the response or perform any necessary actions
        # ...
    
        # Once the request is complete, hide the window
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))
        # Optionally, you can show an error message in the window before closing it
        # ...
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def create_window():
    # ... Window creation code remains the same ...
    def window_proc(hwnd, msg, wparam, lparam):
      if msg == win32con.WM_CLOSE:
          win32gui.DestroyWindow(hwnd)
          return 0
      elif msg == win32con.WM_PAINT:
          hdc, paint_struct = win32gui.BeginPaint(hwnd)
          rect = (20, 20, 180, 80)  # Define the rectangle coordinates
          win32gui.DrawText(hdc, "Loading...", -1, rect, win32con.DT_CENTER)
          win32gui.EndPaint(hwnd, paint_struct)
          return 0
      else:
          return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    # Register the window class
    window_class = win32gui.WNDCLASS()
    window_class.lpfnWndProc = window_proc
    window_class.lpszClassName = "LoadingWindowClass"
    win32gui.RegisterClass(window_class)
    
    # Create the window
    hwnd = win32gui.CreateWindowEx(
        0,
        "LoadingWindowClass",
        "Loading",
        win32con.WS_OVERLAPPEDWINDOW,
        win32con.CW_USEDEFAULT,
        win32con.CW_USEDEFAULT,
        200,
        100,
        0,
        0,
        win32gui.GetModuleHandle(None),
        None
    )
    
    # Show the window
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.UpdateWindow(hwnd)
    
    return hwnd
# Create the loading window
hwnd = create_window()

# Create a thread for sending the request
request_thread = threading.Thread(target=send_request)

# Start the request thread
request_thread.start()

# Wait for the request thread to finish
request_thread.join()

# Both threads have finished, continue with the rest of your code
print("Response received. Continue with the program.")
