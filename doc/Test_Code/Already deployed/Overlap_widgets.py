from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Add a Frame
frame1= Frame(win, bg= "LightPink1")

# Add an optional Label widget
Label(frame1, text= "Welcome Folks!", font= ('Aerial 18 bold italic'), background= "white").pack(pady= 50)
frame1.place(x= 260, y= 50)

# Add a Button widget in second frame
ttk.Button(frame1, text= "Button").place(x= 260, y=50)
win.mainloop()
