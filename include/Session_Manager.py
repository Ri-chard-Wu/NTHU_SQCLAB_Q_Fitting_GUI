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



class Session_Manager:
    def __init__(self, master, gui_mngr):
        self.master = master
        self.gui_mngr = gui_mngr
        self.active = ""
        self.sessions = {}
        self.app = {}
        self.tab_ctrl = ttk.Notebook(master)
        self.tab_ctrl.pack(fill='x')
        
        
        self._init_popup()
    
    def get_active(self):
        return self.sessions[self.active]

    def _init_popup(self):
        self.m = Menu(self.master, tearoff = 0)
        self.m.add_command(label ="Create New Session", command=self.add_session)
        self.m.add_command(label ="Rename", command=self.rename)
        self.m.add_separator()
        self.m.add_command(label ="Cancel")
        self.tab_ctrl.bind("<Button-3>", self.do_popup)
        
    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()
    
    def add_session(self, name=""):
        print("name=", name)
        if(name == ""):
            name = self._get_Untitled_name()

        tab_frame = tk.Frame(self.tab_ctrl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tab_ctrl.add(tab_frame, text = ('  ' + name + '  ') )
        self.tab_ctrl.pack(fill='x')
        self.sessions[name] = tab_frame
        self.active = name
        self.tab_ctrl.select(tab_frame)

        #self.tab_ctrl.config( text="efefe")
        

    def _get_Untitled_name(self):
        def check_collide(name):
            return sum([k==name for k in self.sessions.keys()])
        name = "Untitled"
        i = 1
        while(check_collide(name)):
            name = "Untitled" + "-" + str(i)
            i+=1
        return name
    
    def rename(self):
        self.tab_ctrl.tab("current", text="test")
        #self.tab_ctrl.tab(self.sessions[self.active], text="eeeee")
        #self.popup()