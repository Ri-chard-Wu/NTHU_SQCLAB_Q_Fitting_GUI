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

from Panel_Manager import*
from File_Manager import*
from Fit_Manager import*

PAD_X = 10
SCALE_LEN = 290

class GUI_Manager:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Resonator S21 Fitting")
        self.window.state("zoomed")  #to make it full screen
        self.window.columnconfigure(0, weight=20, minsize=75)

        self.dm = Data_Manager(self)

        self._init_gui()

        self.window.update()
        #print("\nself.topFrame.winfo_width():",self.topFrame.winfo_width(),"\n")
        
        
        self.window.mainloop()

    def plot(self):
        
        self.panel_pm.set_scale_values()
        print("[plot] p=\n",self.dm.para['p'])
        
        self._plot_S21_Fit()
        self._plot_Circle_Fit()

        
        
        '''self.panel_pm.set_scale_values()
        print("[plot] p=\n",self.dm.para['p'])

        self.t1 = Thread(target = self._plot_S21_Fit, args = [])
        self.t1.start()
        
        self.t2 = Thread(target = self._plot_Circle_Fit)
        self.t2.start()'''

    def _plot_S21_Fit(self):
        
        def round_dict(dict, n):
            rounded_dict = {}
            for (k,v) in dict.items():
                rounded_dict[k] = round(v, n)
            return rounded_dict

        def SSE(data ,fit):
            e = data - fit
            e = e/np.mean(data)
            return np.sum(e**2).round(3)

        def to_sci_nota(dict, n):
            def format_e(x,n):
                a = ('%.' + str(n) + 'E') % x
                return a.split('E')[0].rstrip('0').rstrip('.') + ' E' + a.split('E')[1]
            tmp = {}
            for (k,v) in dict.items():
                tmp[k] = format_e(Decimal(str(v)), 3)
            return tmp

        R, I, f = self.dm.data_hdlr['R'], self.dm.data_hdlr['I'], self.dm.data_hdlr['f']
        S21_mag = np.sqrt(R**2 + I**2)
        S21_arg = np.angle(R + 1j*I)
        
       
        p = [v for (k, v) in self.dm.para['p'].items()]
        prc_std = round_dict(self.dm.para['%_std'], 5)
        #print("[plot_S21] p = ",p,"prc_std = ", prc_std)

        
        self.ax1[0][0].clear()
        self.ax1[0][1].clear()
        self.ax1[1][0].clear()
        self.ax1[1][1].clear()


        s = [1 for n in range(len(R))]
      
        #----------------- Upper row ----------------    
        
        self.ax1[0][0].scatter(f, S21_mag, s=s,label='data')
        self.ax1[0][1].scatter(f, S21_arg, s=s,label='data')

        self.ax1[0][0].scatter(f, np.sqrt(Rt(f,*p)**2 + It(f,*p)**2), s=s,label='fit')
        self.ax1[0][1].scatter(f, np.angle(Rt(f,*p) + 1j*It(f,*p)), s=s,label='fit')

        self.ax1[0][0].set_ylabel('mag(S21)')
        self.ax1[0][1].set_ylabel('arg(S21)')

        self.ax1[0][0].title.set_text('SSE = ' + str(SSE(np.sqrt(Rt(f,*p)**2 + It(f,*p)**2), S21_mag)))
        self.ax1[0][1].title.set_text('SSE = ' + str(SSE(np.angle(Rt(f,*p) + 1j*It(f,*p)), S21_arg)))
        
        #------------------ Lower row ---------------    

        self.ax1[1][0].scatter(f, R, s=s,label='data')
        self.ax1[1][1].scatter(f, I, s=s,label='data')

        self.ax1[1][0].scatter(f, Rt(f,*p), s=s,label='fit')
        self.ax1[1][1].scatter(f, It(f,*p), s=s,label='fit')

        self.ax1[1][0].set_ylabel('Re(S21)')
        self.ax1[1][1].set_ylabel('Im(S21)')

        self.ax1[1][0].title.set_text('SSE = ' + str(SSE(R, Rt(f,*p))))
        self.ax1[1][1].title.set_text('SSE = ' + str(SSE(I, It(f,*p))))

        #------------------ --------------- 
       
        self.ax1[0][0].legend()
        self.ax1[0][0].set_xlabel('f(Hz)')
        self.ax1[1][0].legend()
        self.ax1[1][0].set_xlabel('f(Hz)')    
        self.ax1[0][1].legend()
        self.ax1[0][1].set_xlabel('f(Hz)')
        self.ax1[1][1].legend()
        self.ax1[1][1].set_xlabel('f(Hz)')
        
        self.ax1[0][0].locator_params(axis='x', nbins=4)
        self.ax1[0][1].locator_params(axis='x', nbins=4)
        self.ax1[1][0].locator_params(axis='x', nbins=4)
        self.ax1[1][1].locator_params(axis='x', nbins=4)
        
        self.ax1[0][0].grid(True)
        self.ax1[0][1].grid(True)
        self.ax1[1][0].grid(True)
        self.ax1[1][1].grid(True)
        

        def update_Fit_Result_Box():     
            p = to_sci_nota(self.dm.para['p'], 3)
            prc_std = to_sci_nota(self.dm.para['%_std'], 3)
            i = 0
            if(len(self.fit_frame.Fit_Result_Box.get_children(''))):
                for c in self.fit_frame.Fit_Result_Box.get_children(''):
                    self.fit_frame.Fit_Result_Box.delete(c)
            
            for (k, v) in p.items():              
                self.fit_frame.Fit_Result_Box.insert(parent='',index='end', iid=i, text='',values=(k, p[k], prc_std[k]))
                i+=1

        update_Fit_Result_Box()
        #self.fig1.suptitle(title)
    
        self.fig1.tight_layout()
        self.Canvas1.draw()
        
    def _plot_Circle_Fit(self):

        R, I, f = self.dm.data_hdlr['R'], self.dm.data_hdlr['I'], self.dm.data_hdlr['f']
        S21_mag = np.sqrt(R**2 + I**2)
        S21_arg = np.angle(R + 1j*I)
        
        p = [v for (k, v) in self.dm.para['p'].items()]
        
        self.ax2.clear()
        self.ax2.clear()

        s = [1 for n in range(len(R))]
        
        self.ax2.scatter(R, I, s=s, label='data')
        self.ax2.scatter(Rt(f,*p),It(f,*p), s=s,label='fit')

        self.ax2.legend()
        self.ax2.set_xlabel('Re(S21)')
        self.ax2.set_ylabel('Im(S21)')

        self.ax2.locator_params(axis='x', nbins=4)

        self.ax2.grid(True)
   
        self.fig2.tight_layout()
        self.Canvas2.draw()

    '''def _update_Q(self):
            para = self.dm.para
            powers = self.dm.data_hdlr['powers']
            power_selected = powers[self.dm.data_hdlr['data_power']] + "dBm"

            self.dm.para['Q']['Qi'][power_selected] = para['p']['Qi']
            self.dm.para['Q']['Qe'][power_selected] = para['p']['Qe']
            self.dm.para['Q']['Qtot'][power_selected] = para['p']['Qi']* para['p']['Qe']/ (para['p']['Qi']+ para['p']['Qe'])

            #print("\nPop_Q(): Q Saved: Q{}=",self.dm.para['Q'],"\n")
            msg = "Q Saved: Q{}=" + str(self.dm.para['Q'])
            print(msg)

            #self.message_box.insert("end", msg)
            #self.message_box.see("end")
            self.print(msg)'''

    def _update_Q(self):
        para = self.dm.para
        self.dm.para['Q']['Qi'] = para['p']['Qi']
        self.dm.para['Q']['Qe'] = para['p']['Qe']
        self.dm.para['Q']['Qtot'] = para['p']['Qi']* para['p']['Qe']/ (para['p']['Qi']+ para['p']['Qe'])

        #print("\nPop_Q(): Q Saved: Q{}=",self.dm.para['Q'],"\n")
        msg = "Q Saved: Q{}=" + str(self.dm.para['Q'])
        print(msg)

        #self.message_box.insert("end", msg)
        #self.message_box.see("end")
        self.print(msg)

    def print(self, msg):
        msg = ">>> " + msg + "\n"
        self.message_box.insert("end", msg)
        self.message_box.see("end")

    def Plot_Q(self):

        self._update_Q()

        import matplotlib.path as mpath
        star = mpath.Path.unit_regular_star(6)
        circle = mpath.Path.unit_circle()
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
        codes = np.concatenate([circle.codes, star.codes])
        cut_star = mpath.Path(verts, codes)
        

        self.ax3[0].clear()
        self.ax3[1].clear()
        self.ax3[2].clear()

        def convert(Q_dict):
            powers = []
            Q = {'Qi':[],'Qe':[],'Qtot':[]}
            for (power, ds) in self.dm.ds.items():
                powers.append(float(power[:-3]))
                Q['Qi'].append(ds.para['Q']['Qi'])
                Q['Qe'].append(ds.para['Q']['Qe'])
                Q['Qtot'].append(ds.para['Q']['Qtot'])

            return powers, Q

        '''def convert(Q_dict):
            powers = []
            Q = {'Qi':[],'Qe':[],'Qtot':[]}
            for (power, Qi) in Q_dict['Qi'].items():
                powers.append(int(float(power.replace("dBm", ""))))
                Q['Qi'].append(Qi)
            for (power, Qe) in Q_dict['Qe'].items():
                Q['Qe'].append(Qe)
            for (power, Qtot) in Q_dict['Qtot'].items():
                Q['Qtot'].append(Qtot)
            return powers, Q'''

        print("self.dm.para['Q'] = ",self.dm.para['Q'])
        powers, Q = convert(self.dm.para['Q'])
        
        self.ax3[0].set_ylabel('Qi')
        self.ax3[0].set_xlabel('Power (dBm)')
        self.ax3[0].plot(powers, Q['Qi'], marker=cut_star)

        self.ax3[1].set_ylabel('Qe')
        self.ax3[1].set_xlabel('Power (dBm)')
        self.ax3[1].plot(powers, Q['Qe'], marker=cut_star)

        self.ax3[2].set_ylabel('Qtot')
        self.ax3[2].set_xlabel('Power (dBm)')
        self.ax3[2].plot(powers, Q['Qtot'], marker=cut_star)
        
        self.ax3[0].locator_params(axis='x', nbins=4)
        self.ax3[1].locator_params(axis='x', nbins=4)
        self.ax3[2].locator_params(axis='x', nbins=4)


        title = '\nPower Range: ' + str(self.dm.data_hdlr['powers'][-1]) + 'dBm ~ ' + str(self.dm.data_hdlr['powers'][0]) + 'dBm ' 
        self.fig3.suptitle(title)

        print(title,':\n',Q,'\npowers:\n', powers,'\n\n' )

        '''with open(log_file, 'w') as f: 
            json.dump(Q, f)'''

        self.fig3.tight_layout()
        
        self.Canvas3.draw()

    def _init_header_bar(self, master):
        master.pack(fill=X)
        def onOpen():
            self.file_frame.file_open()


            '''file_name = filedialog.askopenfilename(initialdir = "/",title = "Open fitting session",
                                filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"), ("Json File", "*.json")))
            with open(file_name, 'r') as f: 
                session_info = json.load(f)
                print("data opend is: ", session_info)

                
            #print("[onOpen] file_name=", file_name)
            #self.dm.data_hdlr['file_name'] = file_name
            self.dm.read_session(session_info)'''

        def onSave():
            self.file_frame.file_save()
  
        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load fitting session", command=onOpen)
        filemenu.add_command(label="Save fitting session", command=onSave)
        filemenu.add_command(label="Exit", command=self.window.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        

    def _init_top_1(self, master):
        master.pack(side=RIGHT)
        self.tab_Para_Panel, tab = self.tab_wrap(master, 'Fitting Bounds & Parameter Tuning')
        self.panel_pm = Panel_Manager(self, tab , self.dm.para)
        
        
    def _init_top_2(self, master):
        self.plot_frame = master

        plt.ion()

        self.frame_tabControl = master
        self.frame_tabControl.pack(side=RIGHT)
        
        self.tabControl = ttk.Notebook(self.frame_tabControl)

    
        self.tab1 = tk.Frame(self.tabControl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tabControl.add(self.tab1, text ='  S21 Fit  ' )
        self.tabControl.pack(side=RIGHT)

        self.fig1 = plt.Figure(figsize=(8,5.5))
        #NavigationToolbar2Tk(self.fig1, self)
        self.ax1 = [[self.fig1.add_subplot(221), self.fig1.add_subplot(222)],
            [self.fig1.add_subplot(223), self.fig1.add_subplot(224)]] 
        self.Canvas1 = FigureCanvasTkAgg(self.fig1, master = self.tab1)                
        self.Canvas1.get_tk_widget().pack()

        self.tab2 = tk.Frame(self.tabControl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tabControl.add(self.tab2, text ='  Circle Fit  ')
        self.tabControl.pack( side=RIGHT)
        
        self.fig2 = plt.Figure(figsize=(8,5.5))
        self.ax2 = self.fig2.add_subplot(111)
        self.Canvas2 = FigureCanvasTkAgg(self.fig2, master = self.tab2)                
        self.Canvas2.get_tk_widget().pack()


        self.tab3 = tk.Frame(self.tabControl, relief=tk.RAISED,borderwidth=5,fill=None)
        self.tabControl.add(self.tab3, text ='  Q vs Power  ' )
        self.tabControl.pack(side=RIGHT)

        self.fig3 = plt.Figure(figsize=(8,5.5))
        self.ax3 = [self.fig3.add_subplot(131), self.fig3.add_subplot(132), self.fig3.add_subplot(133)]
        self.Canvas3 = FigureCanvasTkAgg(self.fig3, master = self.tab3)                
        self.Canvas3.get_tk_widget().pack()



    def tab_wrap(self, master, name):
        tab_ctrl = ttk.Notebook(master)
        tab_frame = tk.Frame(tab_ctrl, relief=tk.RAISED,borderwidth=5,fill=None)
        tab_ctrl.add(tab_frame, text = ('  ' + name + '  ') )
        #tab_ctrl.pack(side=RIGHT)
        tab_ctrl.pack(fill='x')
        return tab_ctrl, tab_frame



    def _init_log(self, master):
        self.log_frame = master
        self.log_frame.pack(side=RIGHT)




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
        self.message_box.pack()




    def _init_BasicInfo_frame(self, master):
        self.tab_file_frame, tab = self.tab_wrap(master, 'File')
        self.file_frame = File_Frame(tab, self)
        
    def _init_Fit_Frame(self, master):
        self.tab_fit_frame, tab = self.tab_wrap(master, 'Fit')
        self.fit_frame = Fit_Frame(tab, self)

    def _init_top_3(self, master):
        master.pack(side=RIGHT)

        top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        top.pack(side=TOP, fill='x')
        bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        bottom.pack(side=BOTTOM)

        self._init_BasicInfo_frame(top)
        self._init_Fit_Frame(bottom)



    def _init_topFrame(self, master):
        self._init_top_1(tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None))
        self._init_top_2(tk.Frame(master, relief=tk.RAISED,borderwidth=1,fill=None))
        self._init_top_3(tk.Frame(master, relief=tk.RAISED,borderwidth=1,fill=None))



    def _init_Bottom(self, master):
        self._init_log(tk.Frame(master, relief=tk.RAISED,borderwidth=1))
        
        self.button_frame = tk.Frame(master, relief=tk.RAISED,borderwidth=1)
        self.button_frame.pack(side=RIGHT)



    def _init_gui(self):

        topFrame = Frame(self.window)  # Added "container" Frame.
        topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
        Bottom = Frame(self.window, bd=4, relief="ridge")
        Bottom.pack(side=BOTTOM, fill=X, expand=1, anchor=S)

        self._init_topFrame(topFrame)
        self._init_Bottom(Bottom)

        self._init_header_bar(tk.Frame(self.window, relief=tk.RAISED, borderwidth=2))



