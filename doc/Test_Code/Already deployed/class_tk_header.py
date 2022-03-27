import tkinter as tk

class Project_Manager():
    def __init__(self):
        self.window = tk.Tk()
        
    def f1(self):
        window = self.window
        
        def read_scale(scale_value):
            print('scale_value=',scale_value)

        label = tk.Label( text="my_scale").grid(column=0, row=1)
        var = tk.DoubleVar()
        scale = tk.Scale(window, from_=0, to=50, resolution = 0.01,  command=read_scale, variable = var ) 
        scale.grid(column=0, row=0)
        var.set(str(10))

        self.window.mainloop()





























                
