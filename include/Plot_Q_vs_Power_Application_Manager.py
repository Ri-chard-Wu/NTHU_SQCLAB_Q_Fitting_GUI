
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools import Command
import json
import time
from threading import Thread
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from decimal import Decimal

from Data_Manager import *
from File_Manager import*



class Plot_Q_vs_Power_Application_Manager:

    def __init__(self, master, gui_mngr):
        self.window = gui_mngr.window
        self.master = master
        self.app_name = "plot_Q_vs_power"


        self.dm = Data_Manager(self)
        self._init_plot_Q_vs_power_application()
     

    def tab_wrap(self, master, name):
        tab_ctrl = ttk.Notebook(master)
        tab_frame = tk.Frame(tab_ctrl, relief=tk.RAISED,borderwidth=5,fill=None)
        tab_ctrl.add(tab_frame, text = ('  ' + name + '  ') )
        #tab_ctrl.pack(side=RIGHT)
        tab_ctrl.pack(fill='both',expand=True)
        return tab_ctrl, tab_frame
    
    def add_tab(self, tab_ctrl, name):
        
        tab_frame = tk.Frame(tab_ctrl, relief=tk.RAISED,borderwidth=5,fill=None)
        tab_ctrl.add(tab_frame, text = ('  ' + name + '  ') )
        tab_ctrl.pack(fill='x')
        return tab_ctrl, tab_frame

    def _init_log(self, master):
        self.log_frame = master
        self.log_frame.pack(expand = True, fill='both', side=RIGHT)

        self.tab_message_box, tab = self.tab_wrap(self.log_frame, 'System Messages')

        self.message_box = Text( tab ,
                         height='10',
                         width='140',
                         #font=('Consolas 13', 'bold'),
                         font=('TkFixedFont', 11, 'bold')
                         #background="white",
                         #foreground="white",
                         #insertbackground='white'
                         )
        self.message_box.pack(expand = True, fill='both',)

    def _init_BasicInfo_frame(self, master):
        self.tab_file_frame, tab = self.tab_wrap(master, 'File')
        self.file_frame = get_File_Frame(tab, self)
        


    def _init_left(self, master):

        self._init_BasicInfo_frame(master)


    def _init_top_2(self, master):
        self.plot_frame = master

        plt.ion()

        self.frame_tabControl = master
        self.frame_tabControl.pack(side=RIGHT)
        
        self.tabControl = ttk.Notebook(self.frame_tabControl)


        self.tab3 = tk.Frame(self.tabControl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tabControl.add(self.tab3, text ='  Q vs Power  ' )
        self.tabControl.pack(side=RIGHT)

        self.fig3 = plt.Figure(figsize=(11.5, 4.5))
        self.ax3 = [self.fig3.add_subplot(131), self.fig3.add_subplot(132), self.fig3.add_subplot(133)]
        self.Canvas3 = FigureCanvasTkAgg(self.fig3, master = self.tab3)                
        self.Canvas3.get_tk_widget().pack()
        
    def _init_topFrame(self, master):
        self._init_top_2(tk.Frame(master, relief=tk.RAISED,borderwidth=1,fill=None))



    def _init_Bottom(self, master):
        self._init_log(tk.Frame(master, relief=tk.RAISED,borderwidth=1))
    
        self.button_frame = tk.Frame(master, relief=tk.RAISED,borderwidth=1)
        self.button_frame.pack(side=RIGHT)

    def _init_plot_Q_vs_power_application(self):
        left = Frame(self.master)  # Added "container" Frame.
        left.pack(side=LEFT, fill='both', expand=1, anchor=N)
        topFrame = Frame(self.master)  # Added "container" Frame.
        topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
        Bottom = Frame(self.master, bd=4, relief="ridge")
        Bottom.pack(side=BOTTOM, fill=X, expand=1, anchor=S)

        self._init_left(left)
        self._init_topFrame(topFrame)
        self._init_Bottom(Bottom)





    def print(self, msg):
        msg = ">>> " + msg + "\n"
        self.message_box.insert("end", msg)
        self.message_box.see("end")

    def Plot_Q(self, powers, Q ):


        import matplotlib.path as mpath
        star = mpath.Path.unit_regular_star(6)
        circle = mpath.Path.unit_circle()
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
        codes = np.concatenate([circle.codes, star.codes])
        cut_star = mpath.Path(verts, codes)
        

        
        
        self.ax3[0].set_ylabel('Qi')
        self.ax3[0].set_xlabel('Power (dBm)')
        self.ax3[0].plot(powers, Q['Qi'], marker=cut_star)

        self.ax3[1].set_ylabel('Qe')
        self.ax3[1].set_xlabel('Power (dBm)')
        self.ax3[1].plot(powers, Q['Qe'], marker=cut_star)

        self.ax3[2].set_ylabel('Qtot')
        self.ax3[2].set_xlabel('Power (dBm)')
        self.ax3[2].plot(powers, Q['Qtot'], marker=cut_star)
        
        self.ax3[0].locator_params(axis='x', nbins=5)
        self.ax3[1].locator_params(axis='x', nbins=5)
        self.ax3[2].locator_params(axis='x', nbins=5)
        
        self.ax3[0].grid(True)
        self.ax3[1].grid(True)
        self.ax3[2].grid(True)


        #title = '\nPower Range: ' + str(self.dm.data_hdlr['powers'][-1]) + 'dBm ~ ' + str(self.dm.data_hdlr['powers'][0]) + 'dBm ' 
        #self.fig3.suptitle(title)

        #print(title,':\n',Q,'\npowers:\n', powers,'\n\n' )

 

        self.fig3.tight_layout()
        self.Canvas3.draw()

