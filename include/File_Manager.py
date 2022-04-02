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
        v = self.name + " Selected: " + v + "\n\n"
        self.gui_mngr.message_box.insert("end",v)
        


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
        #self._init_info_box()
        


    def _init_dir(self):
        self.self_frame = tk.Frame(self.top,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP, fill="x")

        def browseFiles():
            dirname = filedialog.askdirectory()
            self.gui_mngr.dm.data_hdlr['data_dir'] = dirname
            print("self.gui_mngr.dm.data_hdlr['data_dir'] = ", self.gui_mngr.dm.data_hdlr['data_dir'])
            self.gui_mngr.dm.read_dir()
            self.gui_mngr.message_box.insert("end","Data directory selected: " + dirname + "\n\n")

            #self.f.contents = self.gui_mngr.dm.data_hdlr['file_names']
            #self.f.menu.config(values = self.gui_mngr.dm.data_hdlr['file_names'])
            self.f.refresh_options()
            
            #print("self.f.contents= ",self.f.contents,"\n")
            

        button = Button(self.self_frame, text = "Select a data directory ...", command = browseFiles)
        button.pack(pady=5)



    def _init_DDMenu(self):
        self.f = DDMenu(self.top, self.gui_mngr, "File")
        self.p = DDMenu(self.top, self.gui_mngr, "Power (dBm)")