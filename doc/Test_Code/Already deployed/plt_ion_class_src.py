from plt_ion_class_header import *
import tkinter as tk




pm = PM()
#pm.init_plot()
pm.plot()

window = tk.Tk() 
def replot():
    pm.plot()
       
button = tk.Button(window,text="replot",command=replot)
button.grid(column=2, row=2)
window.mainloop()
