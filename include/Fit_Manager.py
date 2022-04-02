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






class Fit_Button:
    def __init__(self, master, panel_mngr, name):
        self.name = name
        self.panel_mngr = panel_mngr
        button = tk.Button(master, width = 23, height = 2, text = name, command=self.cmd)
        button.pack(side = RIGHT, fill = 'x')

    def cmd(self):
        self.panel_mngr.gui_mngr.dm.Fit(self.name)
        self.panel_mngr.gui_mngr.Plot_Q()
        self.panel_mngr.gui_mngr.plot()

        self.panel_mngr.gui_mngr.dm.save_para()

class Fit_Frame:
    def __init__(self, master, gui_mngr):

        self.gui_mngr = gui_mngr
        self.master = master
        
        self.top = tk.Frame(master)
        self.top.pack(side = TOP)
        self.bottom = tk.Frame(master)
        self.bottom.pack(side = BOTTOM)

        self._init_Fit_Button(self.bottom)
        self._init_info_box(self.top)

    def _init_Fit_Button(self, master):
            top = tk.Frame(master, relief=tk.RAISED, borderwidth=2)
            top.pack(side = TOP, fill = 'x')
            bottom = tk.Frame(master, relief=tk.RAISED, borderwidth=2)
            bottom.pack(side = BOTTOM, fill = 'x')

            
            self.btns = {}
            self.btns["Fit_arg"] =  Fit_Button(top, self, "Fit_arg")
            self.btns["Fit_mag"] =  Fit_Button(top, self, "Fit_mag")
            self.btns["Fit_Im"] =  Fit_Button(bottom, self, "Fit_Im")
            self.btns["Fit_Re"] =  Fit_Button(bottom, self, "Fit_Re")

    def _init_info_box(self, master):
        
        self.Fit_Result_Box = ttk.Treeview(master, height=len(self.gui_mngr.dm.para['p']))
        self.Fit_Result_Box.pack()

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 13))
        style.configure("Treeview", font=(None, 13))
        style.configure('Treeview', rowheight=25)

        self.Fit_Result_Box['columns'] = ('Parameter', 'Fit_Value', '%_std')

        self.Fit_Result_Box.column("#0", width=0,  stretch=NO)
        self.Fit_Result_Box.heading("#0",text="",anchor=CENTER)
        for c in self.Fit_Result_Box['columns']:
            self.Fit_Result_Box.column(c,anchor=CENTER, width=110)
            self.Fit_Result_Box.heading(c,text=c,anchor=CENTER)