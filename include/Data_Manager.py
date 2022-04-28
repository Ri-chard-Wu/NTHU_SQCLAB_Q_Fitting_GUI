import h5py
from idna import check_bidi
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import re
import os
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter import HORIZONTAL, LEFT
from datetime import datetime
import json



data_hdlr = {'data_sel': 3,
        'data_dir': '',
        'data_power': -1,
        'file_names': "",
        'file_name':"",
        'file': 0,
        'log_dir_today':"",
        'R':0,
        'I':0,
        'f':0,
        'powers':0,
        'bg_file_name':'',
        'bg_file':'',
        'bg':{
            'R':0,
            'I':0
        }
 
        
        }
        



para = {     
        'p':{'Qe': 557.442,
             'Qi': 1437.460,
             'f0': 4832501100, #6.59177*10**9,
             #'df': 6.59177*10**9,
             'tau': 1.084,
             'a': 0.0041,
             'alpha': -100.98,
             'Ic': 0.0004,
             'Rc': 0.0004},
        
        '%_std':{},
        
        'LB':{'Qe':600,
              'Qi':500,
              'f0':4733500000,
              #'df':10**8,
              'tau':-1,
              'a':-10,
              'alpha':-120,
              'Ic':-10,
              'Rc':-10},
        
        'UB':{'Qe':1200,
              'Qi':2000,
              'f0':4838500000,
              #'df':10**10,
              'tau':2,
              'a':10,
              'alpha':100,
              'Ic':10,
              'Rc':10},
        'DISCARD_LEFT': 200,
        'DISCARD_RIGHT': 200,
            'Q':{'Qi':0,
             'Qe':0,
             'Qtot':0},
              }
        





class Data_Struct:
    def __init__(self):
        self.para = copy.deepcopy(para)

        '''self.para = {     
        'p':{'Qe':10*10**4,
             'Qi': 35*10**4,
             'f0': 0, #6.59177*10**9,
             #'df': 6.59177*10**9,
             'tau': -105,
             'a': 0.0041,
             'alpha': -100.98,
             'Ic': 0.0004,
             'Rc': 0.0004},
        
        '%_std':{},
        
        'LB':{'Qe':5*10**4,
              'Qi':20*10**4,
              'f0':0,
              #'df':10**8,
              'tau':-200,
              'a':-10,
              'alpha':-120,
              'Ic':-10,
              'Rc':-10},
        
        'UB':{'Qe':30*10**4,
              'Qi':70*10**4,
              'f0':10**11,
              #'df':10**10,
              'tau':200,
              'a':10,
              'alpha':100,
              'Ic':10,
              'Rc':10},
        'DISCARD_LEFT': 600,
        'DISCARD_RIGHT': 600,
            'Q':{'Qi':0,
             'Qe':0,
             'Qtot':0},
              }'''
        

        for (k,v) in self.para['p'].items(): # init percentage std for each para to 0.
            self.para['%_std'][k] = 0


import copy
init_para = copy.deepcopy(para)
class Data_Manager():
    def __init__(self,am):
        self.para = copy.deepcopy(para)
        self.data_hdlr = copy.deepcopy(data_hdlr)
        self.ds = {}
        self.am = am


    def save_para(self):
        if(0):
            self.save_Q()

    def check_dict(self, name, dict):
        return sum([x==name for x in dict.keys()])

    def get(self, name):
        
        if(self.check_dict(name, self.para)):
            return self.para[name]
        elif self.check_dict(name, self.para['p']):
            return self.para['p'][name] 

    def denorm_by_bg(self):
        print("[dm.denorm_by_bg] perfrom bg denorm ")
        def convert(R, I):
            return np.sqrt(R**2 + I**2), np.angle(R + 1j*I)
        def reverse(mag, arg):
            S21 = mag * np.exp( 1j * arg )      
            return np.real(S21), np.imag(S21)
            
        mag_raw, arg_raw = convert(self.data_hdlr['R'], self.data_hdlr['I'])
        mag_bg, arg_bg = convert(self.data_hdlr['bg']['R'], self.data_hdlr['bg']['I'])
       
        mag = mag_raw * mag_bg 
        arg = arg_raw + arg_bg
        R, I = reverse(mag, arg)

        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I

    def norm_by_bg(self):
        # assume raw data and bg data all have been read

        def convert(R, I):
            return np.sqrt(R**2 + I**2), np.angle(R + 1j*I)
        def reverse(mag, arg):
            S21 = mag * np.exp( 1j * arg )      
            return np.real(S21), np.imag(S21)
            
        print("[dm.norm_by_bg] Before bg norm: R.shape = ", self.data_hdlr['R'].shape)

        mag_raw, arg_raw = convert(self.data_hdlr['R'], self.data_hdlr['I'])
        mag_bg, arg_bg = convert(self.data_hdlr['bg']['R'], self.data_hdlr['bg']['I'])
        print("[dm.norm_by_bg] mag_raw.shape = ", mag_raw.shape)
        print("[dm.norm_by_bg] arg_bg.shape = ", arg_bg.shape)
        mag = mag_raw / mag_bg 
        arg = arg_raw - arg_bg
        R, I = reverse(mag, arg)

        print("[dm.norm_by_bg] After bg norm: R.shape = ", R.shape)
        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I

    def read_bg(self):
        if(self.data_hdlr['bg_file_name'] != ''):

            file = h5py.File(self.data_hdlr['bg_file_name'],'r')
            self.data_hdlr['bg_file'] = file
            
            R = file['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,1, 0][int(self.para["DISCARD_LEFT"]):][:int(-self.para["DISCARD_RIGHT"])] 
            I = -file['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,0, 0][int(self.para["DISCARD_LEFT"]):][:int(-self.para["DISCARD_RIGHT"])] 
            self.data_hdlr['bg']['R'] = R
            self.data_hdlr['bg']['I'] = I
            print("[dm.read_bg()] bg R shape = ", R.shape)
         
        

    def save_Q(self):
        log_file = self.data_hdlr['log_dir_today'] +'/'+ \
                     '[' +  str(datetime.now())[11:19].replace(':','_').replace(' ','_') + '] '+\
                                        self.data_hdlr['file_name'].split('data')[1][1:-5] + '.json' 
        with open(log_file, 'w') as f: 
            json.dump(self.para['Q'], f)


    def read_dir(self):
        print("read_dir\n")
        
        file_names = [join(self.data_hdlr['data_dir'], f) for f in listdir(self.data_hdlr['data_dir']) if isfile(join(self.data_hdlr['data_dir'], f))]
        self.data_hdlr['file_names'] = file_names
        print("file_names: ",file_names,"\n")
        
        log_dir = (self.data_hdlr['data_dir'] + "/../log/" + (str(datetime.now())[:10].replace(':','-').replace(' ','_')))
        isExist = os.path.exists(log_dir)
        if not isExist:
            os.makedirs(log_dir)
        self.data_hdlr['log_dir_today'] = log_dir



    def read_session(self, session_info):
        self.data_hdlr['file_name'] = session_info['file_name']
        self.data_hdlr['data_dir'] = session_info['data_dir']
        self.am.file_frame.f.cmd(session_info['file_name'].replace(session_info['data_dir'], ""))
        print("--- self.data_hdlr['file_name'] = ",self.data_hdlr['file_name'])
        print("-- self.data_hdlr['data_dir'] = ",self.data_hdlr['data_dir'])
        self.read_dir()

        for (power, ds) in self.ds.items():
            ds.para = session_info[power]


    def read_file(self):
        print("read_file\n")

        file = h5py.File(self.data_hdlr['file_name'],'r')
        self.data_hdlr['file'] = file
        
        #print("[read_file()] file['Instruments'][0][4] = ", file['Instruments'][0][4])

        if(type(file['Instruments'][0][4]) == type(b'')):
            VNA_name = file['Instruments'][0][4].decode('UTF-8')
        elif(type(file['Instruments'][0][4]) == type('')):
            VNA_name = file['Instruments'][0][4]
        
        self.data_hdlr['VNA_name'] = VNA_name

        self._init_powers()
        self._init_Data_Struct()

        self.am.publish("done read file")
    
    def _init_Data_Struct(self):
        for power in self.data_hdlr['powers']:
            self.ds[(power + 'dBm')] = Data_Struct()
            

    def read_power(self):
        power_to_select = self.data_hdlr['powers'][self.data_hdlr['data_power']]
        power_to_select  = str(float(power_to_select) ) + "dBm"
        self.switch_data_struct(power_to_select)
        print("read_power\n")

        file = self.data_hdlr['file']
        VNA_name = self.data_hdlr['VNA_name']

        
        f1 = self.data_hdlr['file']['/Step config/' + VNA_name + ' - Start frequency/Step items'][0][2]
        f2 = self.data_hdlr['file']['/Step config/' + VNA_name + ' - Stop frequency/Step items'][0][2]
        f = np.linspace(f1, f2, file['/Traces/' + VNA_name + ' - S21'].shape[0])[int(self.para["DISCARD_LEFT"]):][:int(-self.para["DISCARD_RIGHT"])] 
        self.data_hdlr['f'] = f

        R = file['/Traces/' + VNA_name + ' - S21'][:,1, self.data_hdlr['data_power']][int(self.para["DISCARD_LEFT"]):][:int(-self.para["DISCARD_RIGHT"])] 
        I = -file['/Traces/' + VNA_name + ' - S21'][:,0, self.data_hdlr['data_power']][int(self.para["DISCARD_LEFT"]):][:int(-self.para["DISCARD_RIGHT"])] 
        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I
        print("[dm.read_power()] R.shape = ", R.shape)

        self._init_para()
        self.am.panel_pm.refresh()
        self.am.publish("done read power")


    def switch_data_struct(self, power_selected):
        print("[switch_data_struct] power_selected = ", power_selected)
        print("[switch_data_struct] Before switching,  self.para['p']['f0']= ", self.para['p']['f0'])
        print("self.ds.keys()", self.ds.keys())
        
        self.para = self.ds[power_selected].para


    def _init_powers(self):
        self.data_hdlr['powers'] = [str(p[0][0]) for p in self.data_hdlr['file']['/Data/Data'][:]]



    def _init_para(self):
        # Auto-locate f0
        #self.para['p']['f0'] = self.data_hdlr['f'][self.data_hdlr['R'].argmin()]
        print()



    def Data_Preprocessing(self):
        R = self.data_hdlr['R']
        I = self.data_hdlr['I']
        f = self.data_hdlr['f']
        
        def Generate_BG(f, bg_phase_psc, bg_phase_pwr):
            f1 = f[0]
            def arg(f):
                return np.exp( -1j * bg_phase_psc * (f - f1) ** bg_phase_pwr  )
            S21_bg = [arg(f) for f in np.linspace(f[0], f[-1], len(f))]
            return S21_bg

        def Denoize(arg, mag, f):
            sel = abs(arg) < 4 # Denoise
            return mag[sel], arg[sel], f[sel]


        mag = np.sqrt(R**2 + I**2) # Transform to (mag, arg)
        arg = np.angle(R + 1j*I)
         
        S21 = mag * np.exp( 1j * arg ) # Transform back to (Re, Im)
        R = np.real(S21)
        I = np.imag(S21)

        self.data_hdlr['R'], self.data_hdlr['I'], self.data_hdlr['f'] = R, I, f
        



    def Fit(self, op=""):
        def check_bounds(p, LB, UB):
            for name, v in p.items():
                if(p[name] < LB[name]):
                    p[name] = LB[name]
                    self.am.print("[Warning] para value < LB detected for the parameter: "+ name + ". Automatically set para value = LB")
                elif(p[name] > UB[name]):
                    p[name] = UB[name]
                    self.am.print("[Warning] para value > UB detected for the parameter: " + name + ". Automatically set para value = UB")
            return p, LB, UB

        R, I, f = self.data_hdlr['R'], self.data_hdlr['I'], self.data_hdlr['f']

        para = self.para
        para['p'], para['LB'], para['UB'] = check_bounds(copy.deepcopy(para['p']), 
                                                         copy.deepcopy(para['LB']), 
                                                         copy.deepcopy(para['UB']) )

        
        p = [v for (k, v) in para['p'].items()]

        upper_bounds = [v for (k, v) in para['UB'].items()]
        lower_bounds = [v for (k, v) in para['LB'].items()]
        bounds=(lower_bounds, upper_bounds)
        

        cov = []
        if(op=="Fit_Re"): p, cov = curve_fit(Rt, f, R, p, bounds=bounds)
        elif(op=="Fit_Im"): p, cov = curve_fit(It, f, I, p, bounds=bounds)
        elif(op=="Fit_arg"): p, cov = curve_fit(arg_t, f, np.angle(R+1j*I), p, bounds=bounds)
        elif(op=="Fit_mag"): p, cov = curve_fit(mag_t, f, np.absolute(R+1j*I), p, bounds=bounds)

        i=0
        for k in self.para['p'].keys():
            self.para['%_std'][k] = abs((np.sqrt(cov[i,i])/p[i])*100)
            i+=1

        i=0
        for k in self.para['p'].keys():
            self.para['p'][k] = p[i]
            i+=1
            
        return self.para


    

def Rt(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc):
    x = (f - f0)/f0
    N = ( Qe + 1j * Qe * Qi * 2*x ) * a * np.exp(1j*(2*np.pi*alpha + tau*f*10**(-9)))
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.real(N/D) + Rc

def It(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc):
    x = (f - f0)/f0 
    N = ( Qe + 1j * Qe * Qi * 2*x ) * a * np.exp(1j*(2*np.pi*alpha + tau*f*10**(-9)))
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.imag(N/D) + Ic

def arg_t(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc):
    R = Rt(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc)
    I = It(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc)
    arg = np.angle(R + 1j*I)
    return arg

def mag_t(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc):
    R = Rt(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc)
    I = It(f, Qe, Qi, f0, tau, a, alpha, Ic, Rc)
    mag = np.absolute(R + 1j*I)
    return mag




class Data_Preprocessing:
    def _init__(self,am):
        self.am = am


    def Denoize(self, arg, mag, f):
        sel = abs(arg) < 4 # Denoise
        return mag[sel], arg[sel], f[sel]

    def Bg_Normalization(self, mag_raw, arg_raw, mag_bg, arg_bg, f):  
        mag = mag_raw / mag_bg 
        arg = arg_raw - arg_bg
        return mag, arg, f




    