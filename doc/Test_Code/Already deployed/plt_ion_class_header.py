from matplotlib import pyplot as plt
import numpy as np

class PM():
    def __init__(self):
        #self.fig = fig
        #self.ax = ax
        self.i = 1
        self.init_plot()
        
    def init_plot(self):
        plt.ion()
        fig, ax = plt.subplots(1,3)
        self.fig = fig
        self.ax = ax
        
    def plot(self):
        self.i +=1
        
        f = np.array([1,2,3,4,5])
        R = f**2
        I = 1/f
        
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()

        self.ax[0].plot(f, R,label='data')
        self.ax[1].plot(f, I,label='data')
        self.ax[2].plot(R, I, label='data')

        self.ax[0].plot(f, R+self.i,label='fit')
        self.ax[1].plot(f, -I*self.i ,label='fit')
        self.ax[2].plot(R, -I,label='fit')

        self.ax[0].set_ylabel('Re(S11)')
        self.ax[1].set_ylabel('Im(S11)')

        self.ax[0].legend()
        self.ax[0].set_xlabel('f(Hz)')
        
        self.ax[1].legend()
        self.ax[1].set_xlabel('f(Hz)')
        
        self.ax[2].legend()
        self.ax[2].set_xlabel('Re(S11)')
        self.ax[2].set_ylabel('Im(S11)')

        self.fig.set_size_inches(12, 5)
        self.fig.tight_layout()


































