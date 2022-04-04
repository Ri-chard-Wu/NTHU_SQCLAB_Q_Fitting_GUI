import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools import Command
from Data_Manager import *
import json
import time
from threading import Thread
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from decimal import Decimal

PAD_X = 10
SCALE_LEN = 290


class Para_Panel:
    '''
    pos: (row, col) of frame
    '''
    def __init__(self, am, master, pos, para, para_name):
        self.am = am
        #self.para = para
        self.para_name = para_name
        self.frame = tk.Frame(master, relief=tk.RAISED, borderwidth=5, width=1600, height=200)
        self.frame.grid(row=pos[0], column=pos[1], padx=5)

        tk.Label(self.frame, text=self.para_name, font=("Arial", 12)).grid(column=15, row=0)

        self._init_button()
        self._init_entry()
        self._init_scale()
        self._init_right_click_menu(self.frame)
        

    def _init_button(self):

        def confirm():
            L = self.entry1.get()
            U = self.entry2.get()
            
            if(not(L=="")):
                self.scale.configure(from_ = L)
                self.am.dm.para['LB'][self.para_name] = int(L)
            if(not(U=="")):
                self.scale.configure(to = U)
                self.am.dm.para['UB'][self.para_name] = int(U)

        self.button = tk.Button(self.frame,text="confirm", font=("Arial", 12),command=confirm)
        self.button.grid(column=48, row=0, padx=5, pady=(5,0))

    def _confirm_bound(self,v):
            L = self.entry1.get()
            U = self.entry2.get()
            
            if(not(L=="")):
                self.scale.configure(from_ = L)
                self.am.dm.para['LB'][self.para_name] = int(L)
            if(not(U=="")):
                self.scale.configure(to = U)
                self.am.dm.para['UB'][self.para_name] = int(U)
            
            msg = self.para_name + " bounds confirmed: " + "UB = " + U + ", LB = " + L
            self.am.print(msg)

    def _init_entry(self):

        self.entry1 = tk.Entry(self.frame, width=10, font = "Helvetica 10 bold",justify="center")
        self.entry1.grid(column=5, row=0)
        self.entry1.insert(0,str(self.am.dm.para['LB'][self.para_name]))
        self.entry1.bind("<Return>", self._confirm_bound)
        tk.Label(self.frame, text="<", font=("Arial", 12)).grid(column=12, row=0)

        self.entry2 = tk.Entry(self.frame, width=10, font = "Helvetica 10 bold",justify="center")
        self.entry2.grid(column=25, row=0)
        self.entry2.insert(0,str(self.am.dm.para['UB'][self.para_name]))
        self.entry2.bind("<Return>", self._confirm_bound)
        tk.Label(self.frame, text="<", font=("Arial", 12)).grid(column=18, row=0)

    def _init_scale(self):

        def read_scale(scale_value):
            self.am.dm.para['p'][self.para_name]=float(scale_value)
            self.am.plot()
            
        self.var = tk.DoubleVar()
        self.scale = tk.Scale(
            master = self.frame,
            orient = HORIZONTAL,
            from_ = self.am.dm.para['LB'][self.para_name],
            to = self.am.dm.para['UB'][self.para_name],
            resolution = (self.am.dm.para['UB'][self.para_name]-self.am.dm.para['LB'][self.para_name])/100000,
            length = SCALE_LEN,
            command = read_scale,
            variable = self.var )
        self.scale.grid(row=1, column=0, columnspan = 50, padx=5, pady=(0, 5))

    def refresh(self):
        
        self.entry1.delete(0, 'end')
        self.entry1.insert(0,str(self.am.dm.para['LB'][self.para_name]))
        self.entry2.delete(0, 'end')
        self.entry2.insert(0,str(self.am.dm.para['UB'][self.para_name]))
    

    def _init_right_click_menu(self, master):
        def f():
            print("eee")
            
        m = Menu(master, tearoff = 0)
        m.add_command(label ="Cut", command = f)
        m.add_command(label ="Copy")
        m.add_separator()
        m.add_command(label ="Rename")
        
        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()
        
        master.bind("<Button-3>", do_popup)



class Panel_Manager:
    def __init__(self, am, master, para):
        self.am = am
        self.master = master
        
        self.top = tk.Frame(master)
        self.top.pack(side = TOP)
        self.bottom = tk.Frame(master)
        self.bottom.pack(side = BOTTOM)

       
        self.panels = {}
        self.n_panels = 0

        self._init_scroll_bar()
        self._init_panel()
        #self._init_Fit_Button(self.bottom)
        self.fine_adjustment()
        
        
    def _init_panel(self):
        for (k,v) in self.am.dm.para['p'].items():
            pos = (self.n_panels, 0)
            #self.panels[k] = Para_Panel(self.am, self.frame, pos, self.am.dm.para, k)
            self.panels[k] = Para_Panel(self.am, self.scrollable_frame, pos, self.am.dm.para, k)
            self.n_panels += 1

    def _init_scroll_bar(self):

        self.frame = tk.Frame(self.top)
        self.frame.pack()
        
        #print("\nself.topFrame.winfo_width():",self.am.topFrame.winfo_width(),"\n")

        self.canvas = tk.Canvas(self.frame, height = 600, width=330)
        self.canvas.pack(side="left", fill="y", expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(self.canvas, fill=None)
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), height=0, width=0, window = self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


    def set_scale_values(self):
        for (k,v) in self.am.dm.para['p'].items():
            self.panels[k].var.set(str(self.am.dm.para['p'][k]))

    def fine_adjustment(self):
        #self.canvas.config(height =self.am.plot_frame.winfo_height() - 45)
        self.canvas.config(height = 530)
    
    def refresh(self):
        self.am.print("refresh panel")
        for (k, v) in self.panels.items():
            self.panels[k].refresh()

