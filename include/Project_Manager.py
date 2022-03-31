import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import re
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter import HORIZONTAL, LEFT
from datetime import datetime


class Project_Manager():
    
    def __init__(self, para, const, data_hdlr):
        self.para = para
        #self.p = para['Qe'], para['Qi'], para['f0'], para['df'],para['a'],para['alpha'],para['Ic']
        self.const = const
        self.data_hdlr = data_hdlr

        #self._init_data_hdlr()
        
        


    def read_dir(self):
        print("read_dir\n")
        #print("self.data_hdlr['data_dir']: ", self.data_hdlr['data_dir'], "\n")
        
        file_names = [join(self.data_hdlr['data_dir'], f) for f in listdir(self.data_hdlr['data_dir']) if isfile(join(self.data_hdlr['data_dir'], f))]
        self.data_hdlr['file_names'] = file_names

        print("file_names: ",file_names,"\n")
        

    def read_file(self):
        print("read_file\n")

        file = h5py.File(self.data_hdlr['file_name'],'r')
        self.data_hdlr['file'] = file
        
        VNA_name = file['Instruments'][0][4].decode('UTF-8')
        self.data_hdlr['VNA_name'] = VNA_name

        self._init_const()
        #self._init_para()
        



    def read_power(self):
        print("read_power\n")

        file = self.data_hdlr['file']
        VNA_name = self.data_hdlr['VNA_name']

        f1 = self.data_hdlr['file']['/Step config/' + VNA_name + ' - Start frequency/Step items'][0][2]
        f2 = self.data_hdlr['file']['/Step config/' + VNA_name + ' - Stop frequency/Step items'][0][2]
        f = np.linspace(f1, f2, file['/Traces/' + VNA_name + ' - S21'].shape[0])
        self.data_hdlr['f'] = f

        R = file['/Traces/' + VNA_name + ' - S21'][:,1, self.data_hdlr['data_power']] # read data
        I = -file['/Traces/' + VNA_name + ' - S21'][:,0, self.data_hdlr['data_power']]
        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I

        self._init_para()


    def _init_const(self):
        
        self.const['N_SAMPLE'] = self.data_hdlr['file']['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'].shape[2]
        
        #match = re.search('[-]?[0-9]*dBm to [-]?[0-9]*dBm', self.data_hdlr['file_names'][self.data_hdlr['data_sel']])
        #self.const['POWER_RANGE'] = self.data_hdlr['file_names'][match.span()[0] : match.span()[1]]
        
        #self.data_hdlr['powers'] = np.linspace(self.const['POWER_HIGH'], self.const['POWER_LOW'], self.const['N_SAMPLE'])

        self.data_hdlr['powers'] = [str(p[0][0]) for p in self.data_hdlr['file']['/Data/Data'][:]]
        #print('powers:', self.data_hdlr['powers'])

    def _init_para(self):
        self.para['p']['f0'] = self.data_hdlr['f'][self.data_hdlr['R'].argmin()]
 


    def _init_data_hdlr(self):
        file_names = [join(self.data_hdlr['data_dir'], f) for f in listdir(self.data_hdlr['data_dir']) if isfile(join(self.data_hdlr['data_dir'], f))]
        self.data_hdlr['file_names'] = file_names
        file = h5py.File(file_names[self.data_hdlr['data_sel']],'r')
        self.data_hdlr['file'] = file
        
        VNA_name = file['Instruments'][0][4].decode('UTF-8')
        self.data_hdlr['VNA_name'] = VNA_name

        f1 = self.data_hdlr['file']['/Step config/' + self.data_hdlr['VNA_name'] + ' - Start frequency/Step items'][0][2]
        f2 = self.data_hdlr['file']['/Step config/' + self.data_hdlr['VNA_name'] + ' - Stop frequency/Step items'][0][2]
        f = np.linspace(f1, f2, file['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'].shape[0])
        self.data_hdlr['f'] = f

        R = file['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,1, self.data_hdlr['data_power']] # read data
        I = -file['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,0, self.data_hdlr['data_power']]
        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I
      

        


 
    def Read_Data(self):
        DISCARD_LEFT = self.data_hdlr['DISCARD_LEFT']
        DISCARD_RIGHT = self.data_hdlr['DISCARD_RIGHT']

        R = self.data_hdlr['file']['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,1, self.data_hdlr['data_power']][DISCARD_LEFT:][:-DISCARD_RIGHT]
        I = -self.data_hdlr['file']['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'][:,0, self.data_hdlr['data_power']][DISCARD_LEFT:][:-DISCARD_RIGHT]
        self.data_hdlr['R'] = R
        self.data_hdlr['I'] = I
        
        f1 = self.data_hdlr['file']['/Step config/' + self.data_hdlr['VNA_name'] + ' - Start frequency/Step items'][0][2]
        f2 = self.data_hdlr['file']['/Step config/' + self.data_hdlr['VNA_name'] + ' - Stop frequency/Step items'][0][2]

        n_data_point = self.data_hdlr['file']['/Traces/' + self.data_hdlr['VNA_name'] + ' - S21'].shape[0]
        df = (f2 - f1)/n_data_point
        f1 = f1 + DISCARD_LEFT*df
        f2 = f2 - DISCARD_RIGHT*df

        f = np.linspace(f1, f2, len(R))
        self.data_hdlr['f'] = f
        

        return R, I, f
 
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

        #mag, arg, f = Denoize(arg, mag, f)
         
        S21 = mag * np.exp( 1j * arg ) # Transform back to (Re, Im)
        R = np.real(S21)
        I = np.imag(S21)

        self.data_hdlr['R'], self.data_hdlr['I'], self.data_hdlr['f'] = R, I, f
        

    '''def Fit(self, fit_R=0, fit_I=0):
        R, I, f = self.data_hdlr['R'], self.data_hdlr['I'], self.data_hdlr['f']

        para = self.para
        p = para['Qe'], para['Qi'], para['f0'], para['df'],para['a'],para['alpha'],para['Ic']
        
        bounds=([    0,     0,      0, -np.inf, -np.inf, -np.inf, -np.inf],
                [10**7, 10**7, 10**11, +np.inf, +np.inf, +np.inf, +np.inf])
        
        
        if(fit_R): p = curve_fit(Rt, f, R, p, bounds=bounds)[0]
        elif(fit_I): p = curve_fit(It, f, I, p, bounds=bounds)[0]
        self.para['Qe'], self.para['Qi'], self.para['f0'], self.para['df'],\
                         self.para['a'], self.para['alpha'], self.para['Ic'] = p'''

    #def Fit(self, fit_R=0, fit_I=0, fit_arg=0, fit_mag = 0):
    def Fit(self, op=""):
        
        R, I, f = self.data_hdlr['R'], self.data_hdlr['I'], self.data_hdlr['f']

        para = self.para
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


    

'''
def Rt(f, Qe, Qi, f0, df, a, alpha, Ic):
    x = (f - f0 - df)/(f0 + df)
    N = ( Qe + 1j * Qe * Qi * (2*x + 2*df/f0) ) * a * np.exp(1j*alpha)
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.real(N/D)

def It(f, Qe, Qi, f0, df, a, alpha, Ic):
    x = (f - f0 - df)/(f0 + df)
    N = ( Qe + 1j * Qe * Qi * (2*x + 2*df/f0) ) * a * np.exp(1j*alpha)
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.imag(N/D) + Ic

def arg(R,I):
    return np.angle(R+1j*I)

'''





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

'''

def Rt(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc):
    x = (f - f0 - df)/(f0 + df)
    N = ( Qe + 1j * Qe * Qi * (2*x + 2*df/f0) ) * a * np.exp(1j*alpha)
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.real(N/D) + Rc

def It(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc):
    x = (f - f0 - df)/(f0 + df)
    N = ( Qe + 1j * Qe * Qi * (2*x + 2*df/f0) ) * a * np.exp(1j*alpha)
    D = Qi + Qe + 1j*2*Qe*Qi*x
    return np.imag(N/D) + Ic

def arg_t(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc):
    R = Rt(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc)
    I = It(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc)
    arg = np.angle(R + 1j*I)
    return arg

def mag_t(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc):
    R = Rt(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc)
    I = It(f, Qe, Qi, f0, df, tau, a, alpha, Ic, Rc)
    mag = np.absolute(R + 1j*I)
    return mag

'''






