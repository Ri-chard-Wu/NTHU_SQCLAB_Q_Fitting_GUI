import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from setuptools import Command
from Project_Manager import *
import json
import time
from threading import Thread
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)


PAD_X = 10
SCALE_LEN = 290




class Para_Panel:
    '''
    pos: (row, col) of frame
    '''
    def __init__(self, gui_mngr, master, pos, para, para_name):
        self.gui_mngr = gui_mngr
        self.para = para
        self.para_name = para_name
        self.frame = tk.Frame(master, relief=tk.RAISED, borderwidth=5, width=1600, height=200)
        self.frame.grid(row=pos[0], column=pos[1], padx=5)

        tk.Label(self.frame, text=self.para_name, font=("Arial", 12)).grid(column=15, row=0)

        self._init_button()
        self._init_entry()
        self._init_scale()
        

    def _init_button(self):

        def confirm():
            L = self.entry1.get()
            U = self.entry2.get()
            
            if(not(L=="")):
                self.scale.configure(from_ = L)
                self.para['LB'][self.para_name] = int(L)
            if(not(U=="")):
                self.scale.configure(to = U)
                self.para['UB'][self.para_name] = int(U)

        self.button = tk.Button(self.frame,text="confirm", font=("Arial", 12),command=confirm)
        self.button.grid(column=48, row=0, padx=5, pady=(5,0))

    def _init_entry(self):
        
        self.entry1 = tk.Entry(self.frame, width=10, font = "Helvetica 10 bold",justify="center")
        self.entry1.grid(column=5, row=0)
        self.entry1.insert(0,str(self.para['LB'][self.para_name]))
        tk.Label(self.frame, text="<", font=("Arial", 12)).grid(column=12, row=0)

        self.entry2 = tk.Entry(self.frame, width=10, font = "Helvetica 10 bold",justify="center")
        self.entry2.grid(column=25, row=0)
        self.entry2.insert(0,str(self.para['UB'][self.para_name]))
        tk.Label(self.frame, text="<", font=("Arial", 12)).grid(column=18, row=0)

    def _init_scale(self):

        def read_scale(scale_value):
            self.para['p'][self.para_name]=float(scale_value)
            self.gui_mngr.plot()
            
        self.var = tk.DoubleVar()
        self.scale = tk.Scale(
            master = self.frame,
            orient = HORIZONTAL,
            from_ = self.para['LB'][self.para_name],
            to = self.para['UB'][self.para_name],
            resolution = (self.para['UB'][self.para_name]-self.para['LB'][self.para_name])/100000,
            length = SCALE_LEN,
            command = read_scale,
            variable = self.var )
        self.scale.grid(row=1, column=0, columnspan = 50, padx=5, pady=(0, 5))
class Panel_Manager:
    
    def __init__(self, gui_mngr, master, para):
        self.gui_mngr = gui_mngr
        self.master = master
        #self.frame = tk.Frame(master, relief=tk.RAISED, borderwidth=5)
        #self.frame.grid(row=0, column=0, padx=5)
        self.para = para
        self.panels = {}
        self.n_panels = 0

        self._init_scroll_bar()
        self._init_panel()
        
        
        
    def _init_panel(self):
        for (k,v) in self.para['p'].items():
            pos = (self.n_panels, 0)
            #self.panels[k] = Para_Panel(self.gui_mngr, self.frame, pos, self.para, k)
            self.panels[k] = Para_Panel(self.gui_mngr, self.scrollable_frame, pos, self.para, k)
            self.n_panels += 1

    def _init_scroll_bar(self):

        self.frame = ttk.Frame(self.master)
        self.frame.pack()
        
        #print("\nself.topFrame.winfo_width():",self.gui_mngr.topFrame.winfo_width(),"\n")

        self.canvas = tk.Canvas(self.frame, height = 600, width=330)
        self.canvas.pack(side="left", fill="y", expand=True)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(self.canvas, relief=tk.RAISED, borderwidth=5, fill=None)
        self.scrollable_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), height=0, width=0, window = self.scrollable_frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        

    def set_scale_values(self):
        for (k,v) in self.para['p'].items():
            self.panels[k].var.set(str(self.para['p'][k]))
        








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
            contents = self.gui_mngr.pm.data_hdlr['file_names']
        elif (self.name == "Power (dBm)"):
            contents = self.gui_mngr.pm.data_hdlr['powers']

        self.menu = OptionMenu(self.self_frame , self.face , *contents, command=self.cmd )
        self.menu.pack(side=RIGHT)


    def update_data_hldr(self, v):
        if (self.name == "File"):
            self.gui_mngr.pm.data_hdlr["file_name"] = v
            self.gui_mngr.pm.read_file()

            self.gui_mngr.basic_info_frame.p.refresh_options()

        elif (self.name == "Power (dBm)"):
            
            power_index = self.gui_mngr.pm.data_hdlr["powers"].index(v)
            self.gui_mngr.pm.data_hdlr['data_power'] = power_index
            print("self.gui_mngr.pm.data_hdlr['data_power']= ",self.gui_mngr.pm.data_hdlr['data_power'],"\n")
            self.gui_mngr.pm.read_power()





class Basic_Info_Frame():
    def __init__(self, master, gui_mngr):
        self.gui_mngr = gui_mngr
        
        self.top = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.top.pack(side=TOP, fill = "x")
        self.bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=1,fill=None)
        self.bottom.pack(side=BOTTOM)
        
        self._init_dir()
        self._init_DDMenu()
        self._init_info_box()
        


    def _init_dir(self):
        self.self_frame = tk.Frame(self.top,relief=tk.RAISED,borderwidth=1)
        self.self_frame.pack(side=TOP, fill="x")

        def browseFiles():
            dirname = filedialog.askdirectory()
            self.gui_mngr.pm.data_hdlr['data_dir'] = dirname
            self.gui_mngr.pm.read_dir()
            self.gui_mngr.message_box.insert("end","Data directory selected: " + dirname + "\n\n")

            #self.f.contents = self.gui_mngr.pm.data_hdlr['file_names']
            #self.f.menu.config(values = self.gui_mngr.pm.data_hdlr['file_names'])
            self.f.refresh_options()
            
            #print("self.f.contents= ",self.f.contents,"\n")
            

        button = Button(self.self_frame, text = "Select a data directory ...", command = browseFiles)
        button.pack(pady=5)



    def _init_DDMenu(self):
        self.f = DDMenu(self.top, self.gui_mngr, "File")
        self.p = DDMenu(self.top, self.gui_mngr, "Power (dBm)")



    def _init_info_box(self):
        self.BasicInfo_box = Text(self.bottom,
                        height='10',
                        width='75',
                        font='Consolas 12',
                        )
        self.BasicInfo_box.pack()






class GUI_Manager:
    '''
        On initialization, gui manager will reading all matadata about the widgets(p
        ositions, size, identities, cmds). Then, it displays the first fit, and then
        wait for user input.
    '''
    def __init__(self, pm):
        self.window = tk.Tk()
        self.window.title("Resonator S21 Fitting")
        self.window.state("zoomed")  #to make it full screen
        self.window.columnconfigure(0, weight=20, minsize=75)

        self.pm = pm

        self._init_gui()

        self.window.update()
        #print("\nself.topFrame.winfo_width():",self.topFrame.winfo_width(),"\n")
        self.panel_pm.canvas.config(height =self.plot_frame.winfo_height() - 15)
        
        self.window.mainloop()

    def plot(self):
        
        self.panel_pm.set_scale_values()
        print("[plot] p=\n",self.pm.para['p'])
        
        self._plot_S21_Fit()
        self._plot_Circle_Fit()

        
        
        '''self.panel_pm.set_scale_values()
        print("[plot] p=\n",self.pm.para['p'])

        self.t1 = Thread(target = self._plot_S21_Fit, args = [])
        self.t1.start()
        
        self.t2 = Thread(target = self._plot_Circle_Fit)
        self.t2.start()'''

    def _plot_S21_Fit(self):
        
        def round_dict(dict, n):
            for (k,v) in dict.items():
                dict[k] = round(v, n)
            return dict

        def SSE(data ,fit):
            e = data - fit
            e = e/np.mean(data)
            return np.sum(e**2).round(3)
        
        R, I, f = self.pm.data_hdlr['R'], self.pm.data_hdlr['I'], self.pm.data_hdlr['f']
        S21_mag = np.sqrt(R**2 + I**2)
        S21_arg = np.angle(R + 1j*I)
        
        
        p = [v for (k, v) in self.pm.para['p'].items()]
        prc_std = round_dict(self.pm.para['%_std'], 5)


        
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

        self.ax1[0][0].set_ylabel('abs(S21)')
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
        
        
        '''p_ = np.array(p).round(2)
        
        title = str(self.pm.data_hdlr['data_power'] + 1) + '/' + str(self.pm.const['N_SAMPLE']) + '\n\n' +\
                        'Qe= ' + str(p_[0]) + ' +/- ' + str(prc_std['Qe']) + '%'\
                ',   ' + 'Qi= ' + str(p_[1])  + ' +/- ' + str(prc_std['Qi']) + '%'\
                ',   ' + 'Qtot= ' + str(round(p_[0]*p_[1]/(p_[0]+p_[1]))) + \
                ',   ' + 'f0= ' + str(p_[2])  + ' +/- ' + str(prc_std['f0']) + '%'\
                '\n\n'+\
                         'tau= ' + str(p_[3])  + ' +/- ' + str(prc_std['tau']) + '%'\
                ',   ' + 'a= ' + str(p_[4])  + ' +/- ' + str(prc_std['a']) + '%'\
                ',   ' + 'alpha= ' + str(p_[5])  + ' +/- ' + str(prc_std['alpha']) + '%'\
                ',   ' + 'Ic= ' + str(p_[6])  + ' +/- ' + str(prc_std['Ic']) + '%'
        self.fig1.suptitle(title)'''
        self.fig1.tight_layout()
        self.Canvas1.draw()
        
    def _plot_Circle_Fit(self):

        R, I, f = self.pm.data_hdlr['R'], self.pm.data_hdlr['I'], self.pm.data_hdlr['f']
        S21_mag = np.sqrt(R**2 + I**2)
        S21_arg = np.angle(R + 1j*I)
        
        p = [v for (k, v) in self.pm.para['p'].items()]
        
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

    def _Save_Q(self):
            #self.pm.data_hdlr['data_power']
            '''
            para = self.pm.para
            self.pm.data_hdlr['Q']['Qi'].append(para['p']['Qi'])
            self.pm.data_hdlr['Q']['Qe'].append(para['p']['Qe'])
            self.pm.data_hdlr['Q']['Qtot'].append(para['p']['Qi']* para['p']['Qe']/ (para['p']['Qi']+ para['p']['Qe']))
            
            #print("\nPop_Q(): Q Saved: Q{}=",self.pm.data_hdlr['Q'],"\n")
            msg = "\nQ Saved: Q{}=" + str(self.pm.data_hdlr['Q']) + "\n"
            print(msg)
            self.message_box.insert("end", msg)
            '''

            para = self.pm.para
            self.pm.data_hdlr['Q']['Qi'][self.pm.data_hdlr['data_power']] = para['p']['Qi']
            self.pm.data_hdlr['Q']['Qe'][self.pm.data_hdlr['data_power']] = para['p']['Qe']
            self.pm.data_hdlr['Q']['Qtot'][self.pm.data_hdlr['data_power']] = para['p']['Qi']* para['p']['Qe']/ (para['p']['Qi']+ para['p']['Qe'])
            
            #print("\nPop_Q(): Q Saved: Q{}=",self.pm.data_hdlr['Q'],"\n")
            msg = "\nQ Saved: Q{}=" + str(self.pm.data_hdlr['Q']) + "\n"
            print(msg)
            self.message_box.insert("end", msg)

    def Plot_Q(self):

        def Q_dict_to_list(Q):
            Q_list = {}
            Q_list['Qe'] = [v for v in Q['Qe'].values()]
            Q_list['Qi'] = [v for v in Q['Qi'].values()]
            Q_list['Qtot'] = [v for v in Q['Qtot'].values()]
            return Q_list

        self._Save_Q()

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



        POWER_LEFT = self.pm.data_hdlr['POWER_LEFT']
        POWER_RIGHT = self.pm.data_hdlr['POWER_RIGHT']
        log_file = self.pm.data_hdlr['log_file']
        data_sel = self.pm.data_hdlr['data_sel']
       
        Q = self.pm.data_hdlr['Q']
        
        powers = np.linspace(POWER_LEFT[data_sel], POWER_RIGHT[data_sel], len(Q['Qe']))
        
        Q = Q_dict_to_list(Q)
        
        self.ax3[0].set_ylabel('Qi')
        self.ax3[0].set_xlabel('Power (dBm)')
        self.ax3[0].plot(powers, Q['Qi'], marker=cut_star)

        self.ax3[1].set_ylabel('Qe')
        self.ax3[1].set_xlabel('Power (dBm)')
        self.ax3[1].plot(powers, Q['Qe'], marker=cut_star)

        self.ax3[2].set_ylabel('Qtot')
        self.ax3[2].set_xlabel('Power (dBm)')
        self.ax3[2].plot(powers, Q['Qtot'], marker=cut_star)
        
        title = '\nPower Range: ' + str(POWER_LEFT[data_sel]) + 'dBm ~ ' + str(POWER_RIGHT[data_sel]) + 'dBm ' 
        self.fig3.suptitle(title)

        print(title,':\n',Q,'\npowers:\n', powers,'\n\n' )

        with open(log_file, 'w') as f: 
            json.dump(Q, f)

        self.fig3.tight_layout()
        
        self.Canvas3.draw()

    def _init_header_bar(self, master):
        master.pack(fill=X)
        def onOpen():
            print(filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))
        
        def onSave():
            print(filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))
  
        menubar = tk.Menu(self.window)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=onOpen)
        filemenu.add_command(label="Save", command=onSave)
        filemenu.add_command(label="Exit", command=self.window.quit)

        menubar.add_cascade(label="File", menu=filemenu)

        self.window.config(menu=menubar)
        



    def _init_top_1(self, master):
        master.pack(side=RIGHT)
        self.panel_pm = Panel_Manager(self, master, self.pm.para)
        #self.panel_pm = Panel_Manager(self, master, self.pm.para)
        
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

        #print("\nmaster.winfo_width():",master.winfo_width(),"\n")
        #print("\nself.tab1.winfo_width():",self.tab1.winfo_width(),"\n")

    def _init_log(self, master):
        self.log_frame = master
        self.log_frame.pack(side=RIGHT)

        self.message_box = Text(self.log_frame,
                         height='10',
                         width='75',
                         font='Consolas 12',
                         #background="white",
                         #foreground="white",
                         #insertbackground='white'
                         )
        self.message_box.pack()


    def _init_BasicInfo_frame(self, master):

        self.basic_info_frame = Basic_Info_Frame(master, self)
        
        
        '''self.BasicInfo_frame = master
        self.BasicInfo_box = Text(self.BasicInfo_frame,
                         height='10',
                         width='75',
                         font='Consolas 12',
                         #background="white",
                         #foreground="white",
                         #insertbackground='white'
                         )
        self.BasicInfo_box.pack()'''

    '''def _init_DDMenu(self, master):
        #def show():
            #label.config( text = clicked.get() )
        def show(v):
            v = v + "\n"
            self.message_box.insert("end",v)

        p = ["Monday","Tuesday","Wednesday"]
        p_v = StringVar()
        p_v.set( "-10dBm" )
        ps = OptionMenu( master , p_v , *p, command=show )
        ps.pack(side=LEFT)


        f = ["Monday","Tuesday","Wednesday"]
        f_v = StringVar()
        f_v.set( "6.59GHz to 6.5912GHz" )
        fs = OptionMenu( master , f_v , *p, command=show )
        fs.pack(side=RIGHT)'''


    def _init_top_3(self, master):
        master.pack(side=RIGHT)

        '''top = tk.Frame(master,relief=tk.RAISED,borderwidth=5,fill=None)
        top.pack(side=TOP)
        bottom = tk.Frame(master,relief=tk.RAISED,borderwidth=5,fill=None)
        bottom.pack(side=BOTTOM)'''

        self._init_BasicInfo_frame(master)
        #self._init_DDMenu(top)





        #self._init_DDMenu()

    def _init_topFrame(self, master):
        self._init_top_1(tk.Frame(master,relief=tk.RAISED,borderwidth=5,fill=None))
        self._init_top_2(tk.Frame(master, relief=tk.RAISED,borderwidth=5,fill=None))
        self._init_top_3(tk.Frame(master, relief=tk.RAISED,borderwidth=5,fill=None))

    def _init_Bottom(self, master):
        self._init_log(tk.Frame(master, relief=tk.RAISED,borderwidth=5))
        
        self.button_frame = tk.Frame(master, relief=tk.RAISED,borderwidth=5)
        self.button_frame.pack(side=RIGHT)




    def _init_gui(self):

        topFrame = Frame(self.window)  # Added "container" Frame.
        topFrame.pack(side=TOP, fill=X, expand=1, anchor=N)
        Bottom = Frame(self.window, bd=4, relief="ridge")
        Bottom.pack(side=BOTTOM, fill=X, expand=1, anchor=S)

        self._init_topFrame(topFrame)
        self._init_Bottom(Bottom)

        self._init_header_bar(tk.Frame(self.window, relief=tk.RAISED, borderwidth=2))

        
        x = 5
        w = 12
        h = 2
        #---------------------------------| Reset_Para Button >
        import copy
        self.init_para = copy.deepcopy(self.pm.para)
        def Reset_Para():
            self.pm.para = copy.deepcopy(self.init_para)
            self.plot()
            
        next_button = tk.Button(self.button_frame, width = w, height = h, text="Reset_Para",command=Reset_Para)
        next_button.grid(column=2, row=2, padx=x)
        #---------------------------------| Previous_power Button >
        def Previous_power():
            self.pm.data_hdlr['data_power']-= 1
            
            R, I, f = self.pm.Read_Data() # Raw data
            S21_mag = np.sqrt(R**2 + I**2)
            S21_arg = np.angle(R + 1j*I)
            
            self.plot()
            
        next_button = tk.Button(self.button_frame, width = w, height = h,text="Previous_power",command=Previous_power)
        next_button.grid(column=0, row=2, padx=x)
        #---------------------------------| New_power Button >
        def Next_power():

            R, I, f = self.pm.Read_Data() # Raw data
            S21_mag = np.sqrt(R**2 + I**2)
            S21_arg = np.angle(R + 1j*I)
            
            self.pm.data_hdlr['data_power']+= 1
            
            
            self.plot()
            
        next_button = tk.Button(self.button_frame, width = w, height = h,text="Next_power",command=Next_power)
        next_button.grid(column=1, row=2, padx=x)

        #---------------------------------| Fit_Re Button >
        def Fit_Re():
            self.pm.Fit(fit_R=1)
            self.Plot_Q()
            self.plot()
            
        next_button = tk.Button(self.button_frame, width = w, height = h,text="Fit_Re",command=Fit_Re)
        next_button.grid(column=0, row=0, padx=x)
        #---------------------------------| Fit_Im Button >
        def Fit_Im():
            self.pm.Fit(fit_I=1)
            self.Plot_Q()
            self.plot()
            
        next_button = tk.Button(self.button_frame, width = w, height = h,text="Fit_Im",command=Fit_Im)
        next_button.grid(column=1, row=0, padx=x)

        #---------------------------------| Fit_arg Button >
        def Fit_arg():
            self.pm.Fit(fit_arg=1)
            self.Plot_Q()
            self.plot()
            
        button = tk.Button(self.button_frame, width = w, height = h,text="Fit_arg",command=Fit_arg)
        button.grid(column=2, row=0, padx=x)
        #---------------------------------| Fit_mag Button >
        def Fit_mag():
            self.pm.Fit(fit_mag=1)
            self.Plot_Q()
            self.plot()
            
        button = tk.Button(self.button_frame, width = w, height = h,text="Fit_mag",command=Fit_mag)
        button.grid(column=3, row=0, padx=x)
        #---------------------------------| Save_Q Button > 
    
   


