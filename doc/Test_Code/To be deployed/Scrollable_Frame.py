from tkinter import *
import tkinter as tk




'''
from tkinter import *
import tkinter as tk
  
class ScrollBar:
    
    def __init__(self):
         
        root = Tk()
        frame = tk.Frame(root,relief=tk.RAISED,borderwidth=5,fill=None)
        frame.grid(row=0, column=0, padx=5)

        
        h = Scrollbar(frame, orient = 'horizontal')
        h.grid(row=5, column=0)
  
        v = Scrollbar(frame)
        v.grid(row=0, column=5)

          
        t = Text(frame, width = 15, height = 15, wrap = NONE,
                 xscrollcommand = h.set,
                 yscrollcommand = v.set)
        for i in range(20):
            t.insert(END,"this is some text\n")
        t.grid(row=0, column=0)

        
        h.config(command=t.xview)
        v.config(command=t.yview)
        
        root.mainloop()
 
s = ScrollBar()

'''













'''

class ScrollBar:
    
    def __init__(self):
         
        root = Tk()
        frame = tk.Frame(root,relief=tk.RAISED,borderwidth=5,fill=None)
        frame.grid(row=0, column=0, padx=5)

        
        h = Scrollbar(frame, orient = 'horizontal')
        #h.pack(side = BOTTOM, fill = X)
        h.grid(row=5, column=0)
  
        v = Scrollbar(frame)
        #v.pack(side = RIGHT, fill = Y)
        v.grid(row=0, column=5)
          
        t = Text(frame, width = 15, height = 15, wrap = NONE,
                 xscrollcommand = h.set,
                 yscrollcommand = v.set)
        for i in range(20):
            t.insert(END,"this is some text\n")
        #t.pack(side=TOP, fill=X)
        t.grid(row=0, column=0, padx=5)
        
        h.config(command=t.xview)
        v.config(command=t.yview)
        
        root.mainloop()
 
s = ScrollBar()


'''
'''
from tkinter import *

root = Tk()
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )

mylist = Listbox(root, yscrollcommand = scrollbar.set )
for line in range(100):
   mylist.insert(END, "This is line number " + str(line))

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()
'''






#https://blog.teclado.com/tkinter-scrollable-frames/

import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)

canvas = tk.Canvas(container, relief=tk.RAISED,borderwidth=5,fill=None)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas, relief=tk.RAISED,borderwidth=5,fill=None)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()



















