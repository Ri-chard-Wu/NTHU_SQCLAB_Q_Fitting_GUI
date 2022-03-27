import tkinter as tk
import sys
sys.path.append(r'../../include')
from GUI_Manager import *

#---------------------------------| GUI Parameters >
Qe_psc = 10**4
Qi_psc = 10**4
df_psc = 10**9
f0_psc = 10**9

Qe = 6.65*10**4
Qi = 24*10**4
f0 = 6.81667*10**9
df = 0
a = 0.0041
alpha = 5
global Ic 
Ic = 0.0004

p =         Qe,    Qi,     f0,      df,       a,   alpha

scale_paras =\
[{'scale_min':0, 'scale_max':50, 'resolution':0.01, 'name': "Qe", 'var_init':p[0], 'psc':Qe_psc},
 {'scale_min':0, 'scale_max':50, 'resolution':0.01, 'name': "Qi", 'var_init':p[1], 'psc':Qi_psc},
 {'scale_min':6.816, 'scale_max':6.817, 'resolution':0.00001, 'name': "f0", 'var_init':p[2], 'psc':f0_psc},
 {'scale_min':0, 'scale_max':10, 'resolution':0.0001, 'name': "df", 'var_init':p[3], 'psc':df_psc},
 {'scale_min':0, 'scale_max':0.01, 'resolution':0.0001, 'name': "a", 'var_init':p[4], 'psc':1},
 {'scale_min':-10, 'scale_max':10, 'resolution':0.01, 'name': "alpha", 'var_init':p[5], 'psc':1},
 {'scale_min':-0.001, 'scale_max':0.001, 'resolution':0.0001, 'name': "Ic", 'var_init':Ic, 'psc':1},]



gui = GUI_Manager()


def make_scale_cmd(name, psc):
    def read_scale(scale_value):
        gui.scale_values[name] = float(scale_value) * psc
        plot()
    return read_scale

for scale_para in scale_paras:
    gui.add_scale(scale_para, cmd = make_scale_cmd(scale_para['name'], scale_para['psc']))

window.mainloop()

































