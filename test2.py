from tkinterweb import HtmlFrame #import the HtmlFrame widget
try:
  import tkinter as tk #python3
except ImportError:
  import tkinter as tk #python2
root = tk.Tk() #create the Tkinter window

### The important part: create the html widget and attach it to the window
myhtmlframe = HtmlFrame(root) #create HTML browser
myhtmlframe.load_html("<h2>Hello, World!</h2>") #Load some HTML code
myhtmlframe.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window

root.mainloop()