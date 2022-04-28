from this import d
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
        self.am = gui_mngr
        self.name = name
        self.contents = [""]

        self.self_frame = tk.Frame(master,relief=tk.RAISED,borderwidth=1)
        #self.self_frame.pack(side=TOP, fill="x")
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
        #print("[DDMenu.cmd] update the dropdown menu face\n")
        print("v = ", v , "type(v) = ", type(v),"\n")
        self.update_data_hldr(v)

        self.face.set( v[:self.DISPLAY_LENGTH] + (" ..." if len(v) > self.DISPLAY_LENGTH else ""))
        v = self.name + " Selected: " + v 
        self.am.print(v)
        


    def refresh_options(self):
        self.menu.destroy()
        if (self.name == "File"):
            file_names = self.am.dm.data_hdlr['file_names']
            data_dir =  self.am.dm.data_hdlr['data_dir']
            contents =  [file_name.replace(data_dir, "") for file_name in file_names]
            
        elif (self.name == "Power (dBm)"):
            contents = self.am.dm.data_hdlr['powers']

        self.menu = OptionMenu(self.self_frame , self.face , *contents, command=self.cmd )
        self.menu.pack(side=RIGHT)


    def update_data_hldr(self, v):
        if (self.name == "File"):
            v = self.am.dm.data_hdlr['data_dir'] + v
            self.am.dm.data_hdlr["file_name"] = v
            print("[update_data_hldr] self.am.dm.data_hdlr['data_dir'] = ",self.am.dm.data_hdlr['data_dir'])
            print("[update_data_hldr] self.am.dm.data_hdlr[\"file_name\"] =",self.am.dm.data_hdlr["file_name"])
            self.am.dm.read_file()

            self.am.file_frame.p.refresh_options()
            

        elif (self.name == "Power (dBm)"):
            
            power_index = self.am.dm.data_hdlr["powers"].index(v)
            self.am.dm.data_hdlr['data_power'] = power_index
            print("self.am.dm.data_hdlr['data_power']= ",self.am.dm.data_hdlr['data_power'],"\n")
            self.am.dm.read_power()
            self.plot_data()
            #self.update_basic_info_box()
    def plot_data(self):
        self.am.plot()



def get_File_Frame(tab, am):
    if (am.app_name == "default"):
        return File_Frame_Default(tab,am)
    if (am.app_name == "plot_Q_vs_power"):
        return File_Frame_Plot_Q_vs_Power(tab,am)







class Label_CheckBox_Pair:
    def __init__(self, master, am, name):
        self.master = master
        self.am = am
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(side=TOP, fill = "x")

        self.value = tk.BooleanVar() 
        self.value.set(False)
         
        self.chk = tk.Checkbutton(self.frame, text='', var=self.value, command = self.cmd) 
        self.chk.pack(side = RIGHT)

        self.name = tk.Label(self.frame, text=name, pady=5)
        self.name.pack(side = LEFT)

    def cmd(self):
        
        if(self.am.app_name == "default"):
            print("[Label_CheckBox_Pair.cmd()] value = ",self.value.get())

            if(self.value.get()):
                self.am.bg_mngr.file_sel_btn["state"] = NORMAL
            else:
                self.am.bg_mngr.file_sel_btn["state"] = DISABLED
                if(self.am.dm.data_hdlr['bg_file_name'] != ''):
                    self.am.dm.denorm_by_bg()
                    self.am.plot()
                    self.am.dm.data_hdlr['bg_file_name'] = ''
                    self.am.bg_mngr.file_sel_btn['text'] = "Select a bg file ..."
                    #print("[cmd] After bg denorm,")
                    



class Bg_File_Manager():
    '''
    - when first time checked, enable file selector button 
    - when data selected, read bg, perform bg norm, and replot the data for the current power
    - when switching to other data power, msg published by dm.read_file() will triger
      bg norm to automatically perform bg norm
    - when unckecked, first check whether bg data has been read. If read, denorm the 
      current data power, and disable file selector button, and set dm.data_hdlr['bg
      _file_name'] = ''

    '''
    def __init__(self, master, am):
        self.am = am
        self.bg_readed = False

        self.top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.top.pack(side=TOP, fill = "x")
        self.mid = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.mid.pack(side=TOP, fill = "x")
        self.bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.bottom.pack(side=TOP, fill = "x")
        
        self._init_checkbox(self.top)
        self._init_file_selector(self.mid)
        #self._init_file_display(self.bottom)
        self._init_subscribe()

    def _init_subscribe(self):
        self.am.subscribe("bg_mngr", self)

    def msg_available(self, msg):
        #print("msg == \"done read file\" = ",(msg == "done read file"))
        if(msg == "done read power"):
            self.lcp.chk['state'] = NORMAL
            #print("self.lcp.value.get() = ",self.lcp.value.get())
            #print("self.bg_readed = ",self.bg_readed)
            if(self.lcp.value.get()):
                if(self.bg_readed):
                    print("[msg_available] perform nrom_by_bg()")
                    self.am.dm.read_bg()
                    self.am.dm.norm_by_bg()
                    self.am.plot()

 

    def _init_checkbox(self, master):
        self.lcp = Label_CheckBox_Pair(master, self.am, "Normalize by Bg")
        self.lcp.chk['state'] = DISABLED
    


    def _init_file_selector(self, master):
        self.self_frame = tk.Frame(master,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP,expand=True, fill="both")

        def select_bg_file():
            filetypes = (
                ('All files', '*.*'),
                ('text files', '*.txt')
            )
            filename = filedialog.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)

            if(filename != ''):
                self.am.dm.data_hdlr['bg_file_name'] = filename # This is found to be absolute path

                print("[select_bg_file] data_hdlr['data_dir'] = ", self.am.dm.data_hdlr['data_dir'])
                print("[select_bg_file] filename = ", filename)

                data_dir = self.am.dm.data_hdlr['data_dir'].replace("/raw", "")
                self.file_sel_btn['text'] = filename.replace(data_dir, "")[:45] + "..."

                self.bg_readed = True
                self.am.dm.read_bg()
                self.am.dm.norm_by_bg()
                self.am.plot()
                self.am.print("Bg file opened: " + filename )
        
        self.file_sel_btn = Button(self.self_frame, text = "Select a bg file ...", command = select_bg_file)
        self.file_sel_btn.pack(pady=5)
        self.file_sel_btn["state"] = DISABLED

    def _init_file_display(self, master):
 
        
      
        label_left = tk.Label(master, text=" Bg File: " )
        label_left.pack(side = LEFT)

        label_right = tk.Label(master, text=self.am.dm.data_hdlr['bg_file_name'][:20] )
        label_right.pack(side = RIGHT, pady=5)




class File_Frame_Default():
    def __init__(self, master, am):
        self.am = am
        
        self.top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.top.pack(side=TOP, fill = "x")
        self.bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.bottom.pack(side=BOTTOM)
        
        self._init_dir()
        self._init_DDMenu()
        self._init_closing_setting()
        #self._init_info_box()
    


    def _init_closing_setting(self):
        self.am.window.protocol("WM_DELETE_WINDOW", self._on_closing)
    


    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save the current state of this fitting session before exiting?"):
            self.file_save()
            self.am.window.destroy()
        else:
            self.am.window.destroy()



    def file_save(self):
        file_name = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if file_name is None:
            return
        file_name = file_name.name
        print("file_name = ", file_name)
        self.am.print(("file_name = " + file_name))

        with open(file_name, 'w') as f: 
            to_save = {}
            to_save['file_name'] = self.am.dm.data_hdlr['file_name']
            to_save['data_dir'] = self.am.dm.data_hdlr['data_dir']
            print("[file_save] self.am.dm.data_hdlr = ", self.am.dm.data_hdlr) 
            for (k, v) in self.am.dm.ds.items(): 
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
        self.am.dm.read_session(session_info)
            


    def _init_dir(self):
        self.self_frame = tk.Frame(self.top,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP,expand=True, fill="both")

        def browseFiles():
            dirname = filedialog.askdirectory()
            if dirname is '':
                return
            #if(dirname)
            self.am.dm.data_hdlr['data_dir'] = dirname
            print("self.am.dm.data_hdlr['data_dir'] = ", self.am.dm.data_hdlr['data_dir'])
            self.am.dm.read_dir()
         
            self.am.print("Data directory selected: " + dirname )


            self.f.refresh_options()
        
        button = Button(self.self_frame, text = "Select a data directory ...", command = browseFiles)
        button.pack(pady=5)



    def _init_DDMenu(self):
        self.f = DDMenu(self.top, self.am, "File")
        self.p = DDMenu(self.top, self.am, "Power (dBm)")



















class File_Frame_Plot_Q_vs_Power():
    def __init__(self, master, am):
        self.am = am
        self.master = master
        
        self.top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.top.pack(side=TOP,fill = "x")
        self.middle = tk.Frame(master,fill=None)
        self.middle.pack(side=TOP, expand = True,fill = "both", padx = 10, pady = 10)
        self.bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.bottom.pack(side=TOP, fill = "x")
        
        self._init_dir()
        #self._init_label_checkbox_pair()
        self._init_closing_setting()
        self._init_file_select_box()
    
    def _init_closing_setting(self):
        self.am.window.protocol("WM_DELETE_WINDOW", self._on_closing)
    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to save the current state of this fitting session before exiting?"):
            self.file_save()
            self.am.window.destroy()
        else:
            self.am.window.destroy()
    def file_save(self):
        file_name = filedialog.asksaveasfile(mode='w', defaultextension=".json")
        if file_name is None:
            return
        file_name = file_name.name
        print("file_name = ", file_name)
        self.am.print(("file_name = " + file_name))

        with open(file_name, 'w') as f: 
            to_save = {}
            to_save['file_name'] = self.am.dm.data_hdlr['file_name']
            to_save['data_dir'] = self.am.dm.data_hdlr['data_dir']
            print("[file_save] self.am.dm.data_hdlr = ", self.am.dm.data_hdlr) 
            for (k, v) in self.am.dm.ds.items(): 
                to_save[k] = v.para  
            print("to_save[k] = ", to_save[k])
            json.dump(to_save, f)
    
    #def extract_Q(self, data):
        #data['Q']

    def load_selected_files(self):
        data = {}
        for file_name in self.am.dm.data_hdlr['file_names']:
            with open(file_name, 'r') as f: 
                
                for (k, v) in json.load(f).items():
                     if 'dBm' in k:
                        data[k] = v
                
        #print("data.keys() = ",data.keys())
        
        powers = []
        Q = {'Qi':[],'Qe':[],'Qtot':[]}
        for (power, dict) in data.items():
            powers.append(float(power[:-3]))
            Q['Qi'].append(dict['Q']['Qi'])
            Q['Qe'].append(dict['Q']['Qe'])
            Q['Qtot'].append(dict['Q']['Qtot'])


        argsort = np.argsort(powers)
        Q['Qi'] = [Q['Qi'][i] for i in argsort]
        Q['Qe'] = [Q['Qe'][i] for i in argsort]
        Q['Qtot'] = [Q['Qtot'][i] for i in argsort]
        powers = [powers[i] for i in argsort]

        self.am.Plot_Q(powers, Q)

        '''print("--- powers = ",powers)
        print("--- Qi = ",Q['Qi'])
        print("--- Qe = ",Q['Qe'])
        print("--- Qtot = ",Q['Qtot'])'''


    def _init_dir(self):
  

        def browseFiles():
            dirname = filedialog.askdirectory()
            if dirname is '':
                return
    
            self.am.dm.data_hdlr['data_dir'] = dirname
            
            self.am.dm.read_dir()
         
            self.am.print("Data directory selected: " + dirname )


            self.display_files()
        
        button = Button(self.top, text = "Select directory...", command = browseFiles)
        button.pack(pady = 5)

    def display_files(self):
        self.LC_pairs = {}
        
        file_names = self.am.dm.data_hdlr['file_names']
        data_dir =  self.am.dm.data_hdlr['data_dir']
        
        for file_name in file_names:
            name =  file_name.replace(data_dir, "") 
            self.LC_pairs[file_name] = Label_CheckBox_Pair(self.middle, self.am, name)

    #def _init_label_checkbox_pair(self):
    def _init_file_select_box(self):

        def delete_unselected_file_name():
            for (file_name, LC_pair) in self.LC_pairs.items():
                #print("LC_pair.value = ", LC_pair.value.get())
                if LC_pair.value.get() == False:
                    #print("file deleted: ", file_name)
                    #print("--------------------- file_name = ", file_name)
                    #print("------------self.am.dm.data_hdlr['file_names']=",self.am.dm.data_hdlr['file_names'])
                    self.am.dm.data_hdlr['file_names'].remove(file_name)

        def ok():
            delete_unselected_file_name()
            #print("[after deleting unselected files] self.am.dm.data_hdlr['file_names']=",self.am.dm.data_hdlr['file_names'])
            self.load_selected_files()
                

        self.button = Button(self.bottom, text = "plot", command = ok)
        self.button.pack(pady=5)








