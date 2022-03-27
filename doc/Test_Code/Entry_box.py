import tkinter as tk

root= tk.Tk()


entry1 = tk.Entry(root)
entry1.pack()

def getSquareRoot ():  
    x1 = entry1.get()
    
    label1 = tk.Label(root, text= float(x1)**0.5).pack()
    
    
button1 = tk.Button(root, text='Get the Square Root', command=getSquareRoot).pack()


root.mainloop()
