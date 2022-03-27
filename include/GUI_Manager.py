import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Project_Manager import *
import json

PAD_X = 10
SCALE_LEN = 200




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
        
        self.entry1 = tk.Entry(self.frame, width=10)
        self.entry1.grid(column=5, row=0)
        tk.Label(self.frame, text="<", font=("Arial", 12)).grid(column=12, row=0)

        self.entry2 = tk.Entry(self.frame, width=10)
        self.entry2.grid(column=25, row=0)
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
            length = 250,
            command = read_scale,
            variable = self.var )
        self.scale.grid(row=1, column=0, columnspan = 50, padx=5, pady=(0, 5))

class Panel_Manager:
    
    def __init__(self, gui_mngr, master, para):
        self.gui_mngr = gui_mngr
        self.frame = tk.Frame(master, relief=tk.RAISED, borderwidth=5)
        self.frame.grid(row=0, column=0, padx=5)
        self.para = para
        self.panels = {}
        self.n_panels = 0
        
        self._init_panel()
        self._init_scroll_bar()
        
        
    def _init_panel(self):
        for (k,v) in self.para['p'].items():
            pos = (self.n_panels, 0)
            self.panels[k] = Para_Panel(self.gui_mngr, self.frame, pos, self.para, k)
            self.n_panels += 1

    def _init_scroll_bar(self):
        self.h = Scrollbar(self.frame, orient = 'horizontal')
        self.h.pack(side = BOTTOM, fill = X)
  
        self.v = Scrollbar(self.frame)
        self.v.pack(side = RIGHT, fill = Y)

        self.h.config(command=t.xview)
        self.v.config(command=t.yview)
        
    def set_scale_values(self):
        for (k,v) in self.para['p'].items():
            self.panels[k].var.set(str(self.para['p'][k]))
        



class GUI_Manager:
    '''
        On initialization, gui manager will reading all matadata about the widgets(p
        ositions, size, identities, cmds). Then, it displays the first fit, and then
        wait for user input.
    '''
    def __init__(self, pm):
        self.window = tk.Tk()
        self.window.columnconfigure(0, weight=20, minsize=75)

        self.pm = pm

        self._init_gui()
        #self._init_interactive_plot()
        
        self.window.mainloop()
        
        
    def plot(self):
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

        self.panel_pm.set_scale_values()
        
        self.ax[0][0].clear()
        self.ax[0][1].clear()
        self.ax[0][2].clear()
        self.ax[1][0].clear()
        self.ax[1][1].clear()
        self.ax[1][2].clear()

        s = [1 for n in range(len(R))]

        #----------------- Upper row ----------------    
        
        self.ax[0][0].scatter(f, S21_mag, s=s,label='data')
        self.ax[0][1].scatter(f, S21_arg, s=s,label='data')
        self.ax[0][2].scatter(R, I, s=s, label='data')

        self.ax[0][0].scatter(f, np.sqrt(Rt(f,*p)**2 + It(f,*p)**2), s=s,label='fit')
        self.ax[0][1].scatter(f, np.angle(Rt(f,*p) + 1j*It(f,*p)), s=s,label='fit')
        self.ax[0][2].scatter(Rt(f,*p),It(f,*p), s=s,label='fit')

        self.ax[0][0].set_ylabel('abs(S21)')
        self.ax[0][1].set_ylabel('arg(S21)')

        self.ax[0][0].title.set_text('SSE = ' + str(SSE(np.sqrt(Rt(f,*p)**2 + It(f,*p)**2), S21_mag)))
        self.ax[0][1].title.set_text('SSE = ' + str(SSE(np.angle(Rt(f,*p) + 1j*It(f,*p)), S21_arg)))
        
        #------------------ Lower row ---------------    

        self.ax[1][0].scatter(f, R, s=s,label='data')
        self.ax[1][1].scatter(f, I, s=s,label='data')
        self.ax[1][2].scatter(R, I, s=s, label='data')

        self.ax[1][0].scatter(f, Rt(f,*p), s=s,label='fit')
        self.ax[1][1].scatter(f, It(f,*p), s=s,label='fit')
        self.ax[1][2].scatter(Rt(f,*p),It(f,*p), s=s,label='fit')

        self.ax[1][0].set_ylabel('Re(S21)')
        self.ax[1][1].set_ylabel('Im(S21)')

        self.ax[1][0].title.set_text('SSE = ' + str(SSE(R, Rt(f,*p))))
        self.ax[1][1].title.set_text('SSE = ' + str(SSE(I, It(f,*p))))

        #------------------ --------------- 
       
        self.ax[0][0].legend()
        self.ax[0][0].set_xlabel('f(Hz)')
        self.ax[1][0].legend()
        self.ax[1][0].set_xlabel('f(Hz)')    
        self.ax[0][1].legend()
        self.ax[0][1].set_xlabel('f(Hz)')
        self.ax[1][1].legend()
        self.ax[1][1].set_xlabel('f(Hz)')
        
        self.ax[0][2].legend()
        self.ax[0][2].set_xlabel('Re(S21)')
        self.ax[0][2].set_ylabel('Im(S21)')
        self.ax[1][2].legend()
        self.ax[1][2].set_xlabel('Re(S21)')
        self.ax[1][2].set_ylabel('Im(S21)')
        
        self.ax[0][0].locator_params(axis='x', nbins=4)
        self.ax[0][1].locator_params(axis='x', nbins=4)
        self.ax[0][2].locator_params(axis='x', nbins=4)
        self.ax[1][0].locator_params(axis='x', nbins=4)
        self.ax[1][1].locator_params(axis='x', nbins=4)
        self.ax[1][2].locator_params(axis='x', nbins=4)
        
        self.ax[0][0].grid(True)
        self.ax[0][1].grid(True)
        self.ax[0][2].grid(True)
        self.ax[1][0].grid(True)
        self.ax[1][1].grid(True)
        self.ax[1][2].grid(True)
        
        #self.fig.set_size_inches(12, 6)

        print("[plot] p=\n",p)
        p_ = np.array(p).round(2)
        
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
        self.fig.suptitle(title)
        self.fig.tight_layout() 
        
    
    def _init_gui(self):
        
        self.panel_frame = frame = tk.Frame(self.window,relief=tk.RAISED,borderwidth=5,fill=None)
        self.panel_frame.grid(row=0, column=1, rowspan = 50, padx=0, pady=5)
        self.panel_pm = Panel_Manager(self, self.panel_frame, self.pm.para)

        self.plot_frame = tk.Frame(self.window,relief=tk.RAISED,borderwidth=5)
        self.plot_frame.grid(row=0, column=0, padx=5, pady=5)
        plt.ion()
        self.fig, self.ax = plt.subplots( 2, 3, figsize=(10,6))
        self.Canvas = FigureCanvasTkAgg(self.fig, master = self.plot_frame)                
        self.Canvas.get_tk_widget().pack()


        self.log_frame = tk.Frame(self.window,relief=tk.RAISED,borderwidth=5)
        self.log_frame.grid(row=2, column=2, padx=5, pady=5)

        self.button_frame = tk.Frame(self.window,relief=tk.RAISED,borderwidth=5)
        self.button_frame.grid(row=1, column=0, padx=5, pady=5)








        
        x = 15
        #---------------------------------| Reset_Para Button >
        import copy
        self.init_para = copy.deepcopy(self.pm.para)
        def Reset_Para():
            self.pm.para = copy.deepcopy(self.init_para)
            self.plot()
            
        next_button = tk.Button(self.button_frame,text="Reset_Para",command=Reset_Para)
        next_button.grid(column=1, row=2, padx=x, pady=20)
        #---------------------------------| Previous_power Button >
        def Previous_power():
            self.pm.data_hdlr['data_power']-= 1
            
            R, I, f = self.pm.Read_Data() # Raw data
            S21_mag = np.sqrt(R**2 + I**2)
            S21_arg = np.angle(R + 1j*I)
            
            self.plot()
            
        next_button = tk.Button(self.button_frame,text="Previous_power",command=Previous_power)
        next_button.grid(column=2, row=2, padx=x)
        #---------------------------------| New_power Button >
        def Next_power():

            R, I, f = self.pm.Read_Data() # Raw data
            S21_mag = np.sqrt(R**2 + I**2)
            S21_arg = np.angle(R + 1j*I)
            
            self.pm.data_hdlr['data_power']+= 1
            
            '''self.pm.Fit(fit_mag=1)
            self.pm.Fit(fit_arg=1)
            self.pm.Fit(fit_R=1)
            self.pm.Fit(fit_R=1)
            self.pm.Fit(fit_I=1)
            self.pm.Fit(fit_I=1)'''
            
            self.plot()
            
        next_button = tk.Button(self.button_frame,text="Next_power",command=Next_power)
        next_button.grid(column=3, row=2, padx=x)

        #---------------------------------| Fit_Re Button >
        def Fit_Re():
            self.pm.Fit(fit_R=1)
            self.plot()
            
        next_button = tk.Button(self.button_frame,text="Fit_Re",command=Fit_Re)
        next_button.grid(column=4, row=2, padx=x)
        #---------------------------------| Fit_Im Button >
        def Fit_Im():
            self.pm.Fit(fit_I=1)
            self.plot()
            
        next_button = tk.Button(self.button_frame,text="Fit_Im",command=Fit_Im)
        next_button.grid(column=5, row=2, padx=x)

        #---------------------------------| Fit_arg Button >
        def Fit_arg():
            self.pm.Fit(fit_arg=1)
            self.plot()
            
        button = tk.Button(self.button_frame,text="Fit_arg",command=Fit_arg)
        button.grid(column=6, row=2, padx=x)
        #---------------------------------| Fit_mag Button >
        def Fit_mag():
            self.pm.Fit(fit_mag=1)
            self.plot()
            
        button = tk.Button(self.button_frame,text="Fit_mag",command=Fit_mag)
        button.grid(column=7, row=2, padx=x)
        #---------------------------------| Save_Q Button > 
    
        def Save_Q():
            print("\nPop_Q(): Before save: Q{}=",self.pm.data_hdlr['Q'],"\n")
            para = self.pm.para
            self.pm.data_hdlr['Q']['Qi'].append(para['p']['Qi'])
            self.pm.data_hdlr['Q']['Qe'].append(para['p']['Qe'])
            self.pm.data_hdlr['Q']['Qtot'].append(para['p']['Qi']* para['p']['Qe']/ (para['p']['Qi']+ para['p']['Qe']))
            print("\nPop_Q(): After save: Q{}=",self.pm.data_hdlr['Q'],"\n")
               
        button = tk.Button(self.button_frame,text="Save_Q",command=Save_Q)
        button.grid(column=8, row=2, padx=x)
        #---------------------------------| Pop_Q Button > 
        def Pop_Q():
            print("\nPop_Q(): Before pop: Q{}=",self.pm.data_hdlr['Q'],"\n")
            Qi = self.pm.data_hdlr['Q']['Qi'].pop()
            Qe = self.pm.data_hdlr['Q']['Qe'].pop()
            Qtot = self.pm.data_hdlr['Q']['Qtot'].pop()
            print("\nPop_Q(): After pop: Q{}=",self.pm.data_hdlr['Q'],"\n")
               
        button = tk.Button(self.button_frame,text="Pop_Q",command=Pop_Q)
        button.grid(column=9, row=2, padx=x)
        #---------------------------------| Plot_Q >
        import matplotlib.path as mpath
        star = mpath.Path.unit_regular_star(6)
        circle = mpath.Path.unit_circle()
        # concatenate the circle with an internal cutout of the star
        verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
        codes = np.concatenate([circle.codes, star.codes])
        cut_star = mpath.Path(verts, codes)
        def Plot_Q():
            POWER_LEFT = self.pm.data_hdlr['POWER_LEFT']
            POWER_RIGHT = self.pm.data_hdlr['POWER_RIGHT']
            log_file = self.pm.data_hdlr['log_file']
            data_sel = self.pm.data_hdlr['data_sel']
            Q = self.pm.data_hdlr['Q']
            
            powers = np.linspace(POWER_LEFT[data_sel], POWER_RIGHT[data_sel], len(Q['Qe']))
            fig, ax = plt.subplots(1, 3)
            
            ax[0].set_ylabel('Qi')
            ax[0].set_xlabel('Power (dBm)')
            ax[0].plot(powers, Q['Qi'], marker=cut_star)

            ax[1].set_ylabel('Qe')
            ax[1].set_xlabel('Power (dBm)')
            ax[1].plot(powers, Q['Qe'], marker=cut_star)

            ax[2].set_ylabel('Qtot')
            ax[2].set_xlabel('Power (dBm)')
            ax[2].plot(powers, Q['Qtot'], marker=cut_star)
            
            fig.set_size_inches(12, 5)
            title = '\nPower Range: ' + str(POWER_LEFT[data_sel]) + 'dBm ~ ' + str(POWER_RIGHT[data_sel]) + 'dBm ' 
            fig.suptitle(title)

            print(title,':\n',Q,'\npowers:\n', powers,'\n\n' )

            with open(log_file, 'w') as f: 
                json.dump(Q, f)

            fig.tight_layout()
            plt.show()
               
        button = tk.Button(self.button_frame,text="Plot_Q",command=Plot_Q)
        button.grid(column=10, row=2, padx=x)








        
