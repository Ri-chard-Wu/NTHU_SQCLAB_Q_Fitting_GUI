import sys
sys.path.append(r'../include/')
#sys.path.append(r'C:/Users/Richard/Desktop/QC lab/Projects/[v4] Resonator project/include')
from Project_Manager import *
from GUI_Manager import *
#---------------------------------| GUI Parameters >

'''
for 6.8165:

0: -10 to -20
1: -20 to -30
2: 10 to -10 (done)
'''
data_hdlr = {'data_sel': 3,
        'data_dir': r'..\data',
        'data_power': -1,
        'file_names': 0,
        'file': 0,
        'R':0,
        'I':0,
        'f':0,
        'powers':0,
        'DISCARD_LEFT': 600,
        'DISCARD_RIGHT': 600,
        'POWER_LEFT': {0:-10, 1:-20, 2:10, 3:-10, 4:-20, 5:10} ,
        'POWER_RIGHT': {0:-20, 1:-30, 2:-10, 3:-20, 4:-30, 5:-10},
        'Q':{'Qi':{},
             'Qe':{},
             'Qtot':{}},
        
        }
data_hdlr['log_file'] = '../log/6p59_to_6p5925_'+ str(data_hdlr['POWER_LEFT'][data_hdlr['data_sel']]) +'dBm'+'_to_' +str(data_hdlr['POWER_RIGHT'][data_hdlr['data_sel']])+'dBm'+'_'+(str(datetime.now())[:19].replace(':','-').replace(' ','_'))+'.json'  




para = {     
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
              'Rc':10}}

const = { 'N_SAMPLE':1,
          'POWER_RANGE':'',
          'POWER_LOW':-10,
          'POWER_HIGH':10}

#-------------- ------------------
'''
para['p'] = {'Qe':10*10**4,
             'Qi': 9*10**4,
             'f0': 6.8168*10**9,
             #'df': 6.59177*10**9,
             'tau': -110,
             'a': 0.0041,
             'alpha': 0.1,
             'Ic': 0.0004,
             'Rc': 0.0004}
para['LB'] =  {'Qe':5*10**4,
              'Qi':5*10**4,
              'f0':0,
              #'df':10**8,
              'tau':-200,
              'a':-10,
              'alpha':-1,
              'Ic':-10,
              'Rc':-10}
para['UB'] = {'Qe':15*10**4,
              'Qi':25*10**4,
              'f0':10**11,
              #'df':10**10,
              'tau':200,
              'a':10,
              'alpha':1,
              'Ic':10,
              'Rc':10}
              '''
'''

para = {     
        'p':{'Qe':10*10**4,
             'Qi': 35*10**4,
             'f0': 6.59177*10**9, 
             'tau': -105,
             'a': 0.0041,
             'alpha': -100.98,
             'Ic': 0.0004,
             'Rc': 0.0004},
        
        '%_std':{},
        
        'LB':{'Qe':5*10**4,
              'Qi':20*10**4,
              'f0':0,
              'tau':-200,
              'a':-10,
              'alpha':-120,
              'Ic':-10,
              'Rc':-10},
        
        'UB':{'Qe':30*10**4,
              'Qi':70*10**4,
              'f0':10**11,
              'tau':200,
              'a':10,
              'alpha':100,
              'Ic':10,
              'Rc':10}}

const = { 'N_SAMPLE':1,
          'POWER_RANGE':'',
          'POWER_LOW':-10,
          'POWER_HIGH':10}

#-------------- ------------------
para['p'] = {'Qe':10*10**4,
             'Qi': 9*10**4,
             'f0': 6.8168*10**9, 
             'tau': -110,
             'a': 0.0041,
             'alpha': 0.1,
             'Ic': 0.0004,
             'Rc': 0.0004}
para['LB'] =  {'Qe':5*10**4,
              'Qi':5*10**4,
              'f0':0,
              'tau':-200,
              'a':-10,
              'alpha':-1,
              'Ic':-10,
              'Rc':-10}
para['UB'] = {'Qe':15*10**4,
              'Qi':25*10**4,
              'f0':10**11,
              'tau':200,
              'a':10,
              'alpha':1,
              'Ic':10,
              'Rc':10}
#--------------------------------
'''

pm = Project_Manager(para, const, data_hdlr)

print(pm.data_hdlr['file_names'])

#pm.Fit(fit_R = 1)

gui_mngr = GUI_Manager(pm) 

gui_mngr.plot()



# ---------<Reference>---------
'''
A list of all keys:
https://www.pythontutorial.net/tkinter/tkinter-event-binding/

'''




















