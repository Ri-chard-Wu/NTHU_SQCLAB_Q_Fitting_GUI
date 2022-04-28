import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from matplotlib.cbook import delete_masked_points
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import wide_to_long
from setuptools import Command




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
        #self.tab_ctrl.bind("<<NotebookTabChanged>>", self.gui_mngr._update_header)
        self.n = 0

        
        self._init_popup()

    
    def get_active(self):
        tab_name = self.tab_ctrl.tab(self.tab_ctrl.select(), "text")
        name = tab_name[3:-3] # remove the space I introduced 
        return name

    def _init_popup(self):
        self.m = Menu(self.master, tearoff = 0)
        #self.m.add_command(label ="Create New Session", command=self.add_session)
        self.m.add_command(label ="Rename", command=self.rename)
        self.m.add_separator()
        self.m.add_command(label ="Delete", command=self.delete_session)
        self.tab_ctrl.bind("<Button-3>", self.do_popup)
        
    def do_popup(self, event):
        #print("=---active:", self.get_active())
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()
    
    def delete_session(self):
        to_delete = self.get_active()
        self.tab_ctrl.forget(self.tab_ctrl.select())
        #print("\n\n[before]self.sessions.keys()=",self.sessions.keys())
        #print("self.app.keys()=",self.app.keys())

        
        if(self.sessions.get(to_delete)): self.sessions.pop(to_delete)
        if(self.app.get(to_delete)): self.app.pop(to_delete)
        
        #print("\n\n[after]self.sessions.keys()=",self.sessions.keys())
        #print("self.app.keys()=",self.app.keys())

    def add_session(self, name=""):
        self.n += 1

        if(name == ""):
            name = self._get_Untitled_name()

        tab_frame = tk.Frame(self.tab_ctrl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tab_ctrl.add(tab_frame, text = ('   ' + name + '   ') )
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
        
        def rename_and_destroy(e=""):
            #print(self.le.entry.get())
            old = self.get_active()
            new = self.le.entry.get()
            print("---old=",old)
            
            self.tab_ctrl.tab (self.sessions[old], text = "   " + new + "   ")

            #print("[rename]self.sessions.keys() = ", self.sessions.keys())
            #print("[rename]self.app.keys() = ",self.app.keys() )
            #print("[rename]old = ",old)
        
        

            if(self.sessions.get(old)):# Just to check existence in dict()
                self.sessions[new] = self.sessions[old]
                self.sessions.pop(old)

            if(self.app.get(old)):
                self.app[new] = self.app[old]
                self.app.pop(old)

                print("[sm.rename()] Before update am: self.app[new].tab_name = ", self.app[new].tab_name)
                self.app[new].tab_name = new
                print("[sm.rename()] After update am: self.app[new].tab_name = ", self.app[new].tab_name)

            
            
            self.popup.destroy()

        self.popup=Toplevel(self.gui_mngr.window)
        self.popup.geometry('210x90')
        self.popup.bind("<Return>", rename_and_destroy)

        container = tk.Frame(self.popup, fill=None, width=100, height=50)
        container.pack()

        top = tk.Frame(container, width=100,fill=None)
        top.pack(side=TOP, expand=True, fill='both')
        bottom = tk.Frame(container,fill=None)
        bottom.pack(side=BOTTOM, fill='x')

        self.le = Label_Entry_Pair(top, "New Name:       ")

        self.popup_destroy_btn=Button(bottom, text='Ok', width= 8,command=rename_and_destroy)
        self.popup_destroy_btn.pack(side=BOTTOM)

        





class Label_Entry_Pair:
    def __init__(self, master, name):
        
        self.master = master
        self.name = name

        self._init_entry()

    def _init_entry(self):
        self.entry = tk.Entry(self.master, width=12, font = "Helvetica 10",justify="left")
        self.entry.pack(side=RIGHT, pady = 16)
        self.entry.bind("<Return>", self.cmd)
        tk.Label(self.master, text=self.name, font=("Arial", 10)).pack(side=LEFT)

    def cmd(self,v):
        print(3)



