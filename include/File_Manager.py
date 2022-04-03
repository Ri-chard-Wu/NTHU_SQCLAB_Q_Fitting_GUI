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
from tkinter import messagebox

PAD_X = 10
SCALE_LEN = 290




class DDMenu():
    def __init__(self, master, gui_mngr, name):
        self.DISPLAY_LENGTH = 25
        self.gui_mngr = gui_mngr
        self.name = name
        self.contents = [""]

        self.self_frame = tk.Frame(master,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP, fill="x")
        
        name = "  " + name + " :   "
        self.label = tk.Label(self.self_frame, text=name, font=("Arial", 12))
        self.label.pack(side = LEFT)
        
        self.face = StringVar()
        #self.face.set( contents[0][:self.DISPLAY_LENGTH] + (" ..." if len(contents[0]) > self.DISPLAY_LENGTH else ""))
        self.face.set("")
        self.menu = OptionMenu(self.self_frame , self.face , *self.contents, command=self.cmd )
        self.menu.pack(side=RIGHT)

    def cmd(self, v):
        print("v = ", v , "\n")
        self.update_data_hldr(v)

        self.face.set( v[:self.DISPLAY_LENGTH] + (" ..." if len(v) > self.DISPLAY_LENGTH else ""))
        v = self.name + " Selected: " + v 
        self.gui_mngr.print(v)
        


    def refresh_options(self):
        self.menu.destroy()
        if (self.name == "File"):
            file_names = self.gui_mngr.dm.data_hdlr['file_names']
            data_dir =  self.gui_mngr.dm.data_hdlr['data_dir']
            contents =  [file_name.replace(data_dir, "") for file_name in file_names]
            
        elif (self.name == "Power (dBm)"):
            contents = self.gui_mngr.dm.data_hdlr['powers']

        self.menu = OptionMenu(self.self_frame , self.face , *contents, command=self.cmd )
        self.menu.pack(side=RIGHT)


    def update_data_hldr(self, v):
        if (self.name == "File"):
            v = self.gui_mngr.dm.data_hdlr['data_dir'] + v
            self.gui_mngr.dm.data_hdlr["file_name"] = v
            self.gui_mngr.dm.read_file()

            self.gui_mngr.file_frame.p.refresh_options()
            

        elif (self.name == "Power (dBm)"):
            
            power_index = self.gui_mngr.dm.data_hdlr["powers"].index(v)
            self.gui_mngr.dm.data_hdlr['data_power'] = power_index
            print("self.gui_mngr.dm.data_hdlr['data_power']= ",self.gui_mngr.dm.data_hdlr['data_power'],"\n")
            self.gui_mngr.dm.read_power()
            self.plot_data()
            #self.update_basic_info_box()


        
    def plot_data(self):
        self.gui_mngr.plot()





class File_Frame():
    def __init__(self, master, gui_mngr):
        self.gui_mngr = gui_mngr
        
        self.top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.top.pack(side=TOP, fill = "x")
        self.bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.bottom.pack(side=BOTTOM)
        
        self._init_dir()
        self._init_DDMenu()
        self._init_closing_setting()
        #self._init_info_box()
    
    def _init_closing_setting(self):
        self.gui_mngr.window.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save the current state of this fitting session before exiting?"):
            self.file_save()
            self.gui_mngr.window.destroy()
        else:
            self.gui_mngr.window.destroy()

    def file_save(self):
        file_name = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if file_name is None:
            return
        file_name = file_name.name
        print("file_name = ", file_name)
        self.gui_mngr.print(("file_name = " + file_name))

        with open(file_name, 'w') as f: 
            to_save = {}
            to_save['file_name'] = self.gui_mngr.dm.data_hdlr['file_name']
            to_save['data_dir'] = self.gui_mngr.dm.data_hdlr['data_dir']
            print("[file_save] self.gui_mngr.dm.data_hdlr = ", self.gui_mngr.dm.data_hdlr) 
            for (k, v) in self.gui_mngr.dm.ds.items(): 
                to_save[k] = v.para  
            print("to_save[k] = ", to_save[k])
            json.dump(to_save, f)
    
    def file_open(self):
        file_name = filedialog.askopenfilename(initialdir = "/",title = "Open fitting session",
                            filetypes = (("Json File", "*.json"),("Python files","*.py;*.pyw"),("All files","*.*")))
        if file_name is '':
            return
        with open(file_name, 'r') as f: 
            session_info = json.load(f)
            print("data opend is: ", session_info)

            
        #print("[onOpen] file_name=", file_name)
        #self.dm.data_hdlr['file_name'] = file_name
        self.gui_mngr.dm.read_session(session_info)
            
    def _init_dir(self):
        self.self_frame = tk.Frame(self.top,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP, fill="x")

        def browseFiles():
            dirname = filedialog.askdirectory()
            if dirname is '':
                return
            #if(dirname)
            self.gui_mngr.dm.data_hdlr['data_dir'] = dirname
            print("self.gui_mngr.dm.data_hdlr['data_dir'] = ", self.gui_mngr.dm.data_hdlr['data_dir'])
            self.gui_mngr.dm.read_dir()
         
            self.gui_mngr.print("Data directory selected: " + dirname )


            self.f.refresh_options()
            
      
            

        button = Button(self.self_frame, text = "Select a data directory ...", command = browseFiles)
        button.pack(pady=5)



    def _init_DDMenu(self):
        self.f = DDMenu(self.top, self.gui_mngr, "File")
        self.p = DDMenu(self.top, self.gui_mngr, "Power (dBm)")