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
        self.panel_mngr.am.dm.Fit(self.name)
        self.panel_mngr.am.Plot_Q()
        self.panel_mngr.am.plot()

        self.panel_mngr.am.dm.save_para()





        
class Fit_Frame:
    def __init__(self, master, am):

        self.am = am
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
        
        self.Fit_Result_Box = ttk.Treeview(master, height=len(self.am.dm.para['p']))
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
        
        self._add_right_click_popup(self.Fit_Result_Box)

    def _add_right_click_popup(self, master):
        #def do_popup(event):  
                #popup = popupWindow(master)
        master.bind("<Button-1>", self.do_popup)



    def do_popup(self, e):

        self.popup=Toplevel(self.am.window)

        self.popup_destroy_btn=Button(self.popup,text='Ok',command=self.popup.destroy)
        self.popup_destroy_btn.pack(side=BOTTOM)

        self._init_label_entry_pair(self.popup)


    def _init_label_entry_pair(self, master):
        self.LE_pairs = {}
        to_init = [name for name in self.am.dm.para['p'].keys()]
        for name in to_init:
            top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
            top.pack(side=TOP, fill='x')
            self.LE_pairs[name] = Label_Entry_Pair(top, self.am, name)
        

    def update_Fit_Result_Box(self):   

        def to_sci_nota(dict, n):
            def format_e(x,n):
                a = ('%.' + str(n) + 'E') % x
                return a.split('E')[0].rstrip('0').rstrip('.') + ' E' + a.split('E')[1]
            tmp = {}
            for (k,v) in dict.items():
                tmp[k] = format_e(Decimal(str(v)), 3)
            return tmp

        p = to_sci_nota(self.am.dm.para['p'], 3)
        prc_std = to_sci_nota(self.am.dm.para['%_std'], 3)
        i = 0
        if(len(self.Fit_Result_Box.get_children(''))):
            for c in self.Fit_Result_Box.get_children(''):
                self.Fit_Result_Box.delete(c)
        
        for (k, v) in p.items():              
            self.Fit_Result_Box.insert(parent='',index='end', iid=i, text='',values=(k, p[k], prc_std[k]))
            i+=1



class Label_Entry_Pair:
    def __init__(self, master, am, name):
        
        self.master = master
        self.name = name
        self.am = am

        self._init_entry()

    def _init_entry(self):
        self.entry = tk.Entry(self.master, width=10, font = "Helvetica 10 bold",justify="center")
        self.entry.pack(side=RIGHT)
        self.entry.insert(0, str(self.am.dm.get(self.name)))
        self.entry.bind("<Return>", self.cmd)
        tk.Label(self.master, text=self.name, font=("Arial", 12)).pack(side=LEFT)

    def cmd(self,v):
        value = self.entry.get()
        self.am.dm.para[self.name] = float(value)
        self.am.dm.read_power()
        self.am.plot()
        msg = self.name + " value confirmed: " + str(value)
        self.am.print(msg)        
        print("self.am.dm.para = ", self.am.dm.para)


class Config_Frame:
    def __init__(self, master, am):
        
        self.master = master
        self.am = am
        self.LE_pairs = {}

        self._init_label_entry_pair()
    
    def _init_label_entry_pair(self):
        to_init = ["DISCARD_LEFT", "DISCARD_RIGHT"]
        for name in to_init:
            top = tk.Frame(self.master,relief=tk.RAISED,borderwidth=1,fill=None)
            top.pack(side=TOP, fill='x')
            self.LE_pairs[name] = Label_Entry_Pair(top, self.am, name)


