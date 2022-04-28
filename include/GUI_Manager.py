

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
        
        self.subscriber = []

        self.window.update()
        #print("\nself.topFrame.winfo_width():",self.topFrame.winfo_width(),"\n")
        self.window.bind('<Control-z>', self.publish_ctrl_z)
        self.window.bind('<Control-y>', self.publish_ctrl_y) 
        self.window.mainloop()
        


    #def undo(self, v):
        #print("crtl-z detected, v.keysym = ", v.keysym)
    def subscribe(self, object):
        self.subscriber.append(object)

    def publish_ctrl_z(self, _):
        self.publish("ctrl_z pressed")
    
    def publish_ctrl_y(self, _):
        self.publish("ctrl_y pressed")
    
    def publish(self, msg):
        for object in self.subscriber:
            object.msg_available(msg)




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
        #print("---- check_accessibilit")
        
        if(self.sm.n):
            self.option.entryconfigure('Default application', state=tk.NORMAL)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.NORMAL)
        else:
            self.option.entryconfigure('Default application', state=tk.DISABLED)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.DISABLED)
        #print("--- self.sm.app.keys() =", self.sm.app.keys() )
        #print("--- self.sm.get_active() = ", self.sm.get_active())
        if(self.sm.app.get(self.sm.get_active())): # check whether name exist at all.
            #print("----name exist")
            self.option.entryconfigure('Default application', state=tk.DISABLED)
            self.option.entryconfigure('Plot Q vs Power application', state=tk.DISABLED)

            if(self.sm.app[self.sm.get_active()].app_name == "default"):
                #print("--self.sm.app[self.sm.get_active()].dm.data_hdlr['data_dir']=",self.sm.app[self.sm.get_active()].dm.data_hdlr['data_dir'])
                
                self.filemenu.entryconfigure('Load session data', state=tk.NORMAL)
                self.filemenu.entryconfigure('Save session data', state=tk.NORMAL)
                if(self.sm.app[self.sm.get_active()].dm.data_hdlr['data_dir'] != ""):
                    self.filemenu.entryconfigure('Load session data', state=tk.DISABLED)
            else:
                self.filemenu.entryconfigure('Load session data', state=tk.DISABLED)
                self.filemenu.entryconfigure('Save session data', state=tk.DISABLED)
        else:
            self.filemenu.entryconfigure('Load session data', state=tk.DISABLED)
            self.filemenu.entryconfigure('Save session data', state=tk.DISABLED)


    def _create_session(self):
        self.sm.add_session()

        
 
    def _launch_default_application(self):
        self.sm.app[self.sm.get_active()] = Default_Application_Manager(self.sm.sessions[self.sm.get_active()], self, self.sm)
        print("self.sm.active=",self.sm.get_active())



    def _launch_plot_Q_vs_power_application(self):
        self.sm.app[self.sm.get_active()] = Plot_Q_vs_Power_Application_Manager(self.sm.sessions[self.sm.get_active()], self)
        print("self.sm.active=",self.sm.get_active())

        

