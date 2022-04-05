

from Session_Manager import*
from Default_Application_Manager import*
from Plot_Q_vs_Power_Application_Manager import*




class GUI_Manager:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Resonator S21 Fitting")
        self.window.state("zoomed")  #to make it full screen
        self.window.columnconfigure(0, weight=20, minsize=75)

        self.dm = Data_Manager(self)
        self.sm = Session_Manager(self.window, self)
        self._init_header_bar(tk.Frame(self.window, relief=tk.RAISED, borderwidth=2))
        #self._create_session()
     
        self.window.update()
        #print("\nself.topFrame.winfo_width():",self.topFrame.winfo_width(),"\n")
        
        self.window.mainloop()

    def _init_header_bar(self, master):
        master.pack(fill=X)
        def onOpen():
            self.sm.app[self.sm.get_active()].file_frame.file_open()

        def onSave():
            print("[onSave] self.sm.get_active() = ", self.sm.get_active())
            #print("self.sm.tab_ctrl.tab(self.sm.tab_ctrl.select(), \"text\") = ", )
            self.sm.app[self.sm.get_active()].file_frame.file_save()
      
        menubar = tk.Menu(self.window)
        menubar.bind("<<MenuSelect>>", self.check_accessibility)

        self.filemenu = tk.Menu(menubar, tearoff=0)
        self.filemenu.add_command(label="New session", command=self._create_session)
        self.filemenu.add_command(label="Load session data", command=onOpen, state = 'disabled')
        self.filemenu.add_command(label="Save session data", command=onSave, state = 'disabled')
        menubar.add_cascade(label="File", menu=self.filemenu)

        #filemenu.entryconfigure('Load session data', state=tk.NORMAL)
        

        self.option = tk.Menu(menubar, tearoff=0)
        self.option.add_command(label="Default application", command=self._launch_default_application, state = 'disabled')
        self.option.add_command(label="Plot Q vs Power application", command=self._launch_plot_Q_vs_power_application, state = 'disabled')
        menubar.add_cascade(label="Launch", menu=self.option)

  
        self.window.config(menu=menubar)
        

    def check_accessibility(self,event):
        
        if(self.sm.n):
            self.option.entryconfigure('Default application', state=tk.NORMAL)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.NORMAL)
        else:
            self.option.entryconfigure('Default application', state=tk.DISABLED)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.DISABLED)

        if(self.sm.app.get(self.sm.get_active())): # check whether name exist at all.
            
            self.option.entryconfigure('Default application', state=tk.DISABLED)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.DISABLED)

            if(self.sm.app[self.sm.get_active()].app_name == "default"):
                self.filemenu.entryconfigure('Load session data', state=tk.NORMAL)
                self.filemenu.entryconfigure('Save session data', state=tk.NORMAL)
            else:
                self.filemenu.entryconfigure('Load session data', state=tk.DISABLED)
                self.filemenu.entryconfigure('Save session data', state=tk.DISABLED)
        else:
            self.filemenu.entryconfigure('Load session data', state=tk.DISABLED)
            self.filemenu.entryconfigure('Save session data', state=tk.DISABLED)


    def _create_session(self):
        self.sm.add_session()

        
 
    def _launch_default_application(self):
        self.sm.app[self.sm.get_active()] = Default_Application_Manager(self.sm.sessions[self.sm.get_active()], self)
        print("self.sm.active=",self.sm.get_active())



    def _launch_plot_Q_vs_power_application(self):
        self.sm.app[self.sm.get_active()] = Plot_Q_vs_Power_Application_Manager(self.sm.sessions[self.sm.get_active()], self)
        print("self.sm.active=",self.sm.get_active())

        

