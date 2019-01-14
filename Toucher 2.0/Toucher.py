import tkinter
from tkinter import ttk
import os
import webbrowser
from tkinter.messagebox import *
from tkinter import ttk
import tkinter.filedialog
import pythoncom, pyHook
import _thread
import keyboard
import time
import ctypes
import pyperclip
from win32gui import GetWindowText, GetForegroundWindow




class FInal_AI:
    def show_window(self):
        help_window = tkinter.Tk()
        f = open(self.database_file, 'r')
        tv = ttk.Treeview(help_window)
        tv['columns'] = ('Nick Name', 'File path')
        tv.heading('Nick Name', text='Nick Name')
        tv.column('Nick Name', anchor='w', width=100)
        tv.heading('File path', text='File path')
        tv.column('File path', width=200, anchor='w')
        tv['show'] = 'headings'  
        tv.grid(row=0)
        for row in f:
            t = row.split(",")
            nick_name = t[0]
            nick_name = nick_name.replace(" ", "_")
            x = nick_name + " " + str(t[1])
            tv.insert('', 'end', values=(x))
        help_window.mainloop()
        
        
    def check_dir_path(self,database):
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
         
        titles = []
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, buff, length + 1)
                titles.append(buff.value)
            return True
        EnumWindows(EnumWindowsProc(foreach_window), 0)

        tab_count=0
        flag=0
        titles=list(filter(None,titles))
        titles.pop(0)
        titles.pop(-1)
        for i in titles:
            i=i.split("-")
            tab_count+=1
            if(len(i)==1):
                break
        user32 = ctypes.windll.user32
        
        user32.keybd_event(0x12, 0, 0, 0) #Alt
        user32.keybd_event(0x09, 0, 0, 0) #Tab
        time.sleep(0.1)
        user32.keybd_event(0x09, 0, 2, 0) #~Tab
        for i in range(tab_count-1):
            user32.keybd_event(0x09, 0, 0, 0) #Tab
            time.sleep(0.1)
            user32.keybd_event(0x09, 0, 2, 0) #~Tab
            
        user32.keybd_event(0x12, 0, 2, 0) #~Alt   
        time.sleep(0.1)
        keyboard.press_and_release('alt+d')
        pyperclip.copy(database[self.get_path])
        keyboard.press_and_release('ctrl+v')
        keyboard.press_and_release('enter')                        
        self.open_path.delete(0, 'end')
                
    def exit_window(self):
        self.window.destroy()
        

    def write_macro(self,x):
        keyboard.play(x, speed_factor=1.0)    
    
    def check_pass(self):
        database=dict()
        with open(self.database_file, 'r') as f:
                for row in f:
                    self.database.append(row)
                    if (row is not "\n"):
                        row = row.rstrip()
                        row = row.split(",")
                        database.update({row[0]: row[1]})
                f.close()
        #print(database)
        if('pass' in database.keys()):
            self.open_path.delete(0, 'end')
            if(database['pass']==self.get_path):
                self.open_path.insert(0,'Successfull!')
            else:
                self.open_path.insert(0,'Invalid Password!!')
        else:
            self.write_path_to_database(self.get_path,'pass')
            self.open_path.insert(0,'Updated new Password!!')
    
    def prev_args_list(self):
        #print(self.get_path)
        if(self.prev_args[0]=='set:'):
            if(self.prev_args[1]=='pass:'):
                self.check_pass()
            
        
        self.open_path.configure(show='')
        return
    
    def open_path_function(self):
        #print("was here")
        self.get_path=self.open_path.get()
        if(self.additional_args==1):
            self.additional_args=0
            self.prev_args_list()
            return

            

        if(self.get_path=='exit'):
            self.exit_window()
            exit()
            
        elif(self.get_path=='help'):
            self.show_window()
            
        elif(self.get_path=='check'):
            self.check_dir_path()
            
        elif('macro' in self.get_path):
            self.get_path=self.get_path.strip('macro: ')
            self.open_path.delete(0, 'end')
            if(self.get_path in self.macro_dict.keys()):
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, 'Key already present!')
            else:
                x=keyboard.record(until='escape', suppress=False, trigger_on_release=False)
                #print(type(x))
                self.macro_dict[self.get_path]=x
                #print(self.macro_dict,x)
                self.open_path.delete(0, 'end')
                self.open_path.insert(0,'Macro-recorded as: ' + str(self.get_path))
            return
            
            
        elif("exe: " in self.get_path):
            self.get_path=self.get_path.split(' ')
            #print("the key is ", self.get_path[1])
            if(self.get_path[1] not in self.macro_dict.keys()):
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, 'Key does not exist!')
            else:
                self.open_path.delete(0, 'end')
                time.sleep(3)
                keyboard.play(self.macro_dict[self.get_path[1]], speed_factor=1.0)
                self.open_path.insert(0, 'Macro \'{}\' Executed!'.format(self.get_path[1]))
            return
        elif(self.get_path=="exit macro"):
            self.open_path.delete(0, 'end')
            return
            
            
        elif("del: " in self.get_path):
            self.get_path=self.get_path.split(' ')
            if(self.get_path[1] not in self.macro_dict.keys()):
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, 'Key does not exist!')
            else:
                self.macro_dict.pop(self.get_path[1])
                self.open_path.insert(0, 'Macro {} deleted'.format(self.open_path[1]))
            return
            
        # Setting menu   
        elif("set:" in self.get_path):
            #print("Here")
            self.get_path=self.get_path.split(' ')
            if(self.get_path[1]=='color:'):
                #print(self.get_path[2])
                #self.get_path=self.get_path.split(' ')
                #print(self.get_path)
                try:
                    self.open_path['background']=self.background_color[self.get_path[2]]
                    self.open_path.delete(0, 'end')
                except:
                    self.open_path.delete(0, 'end')
                    self.open_path.insert(0, "Invalid color option")
                #print(self.get_path)
            
            
            
            elif('pass:' in self.get_path[1]):
                self.open_path.delete(0, 'end')
                self.open_path.configure(show='*')
                self.additional_args=1
                self.prev_args=self.get_path
                #print(self.get_path)
                
            
            # if empty setting
            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Please pass -args")
            
                
            return
            
        
        elif("G:" in self.get_path):
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
            GetWindowText = ctypes.windll.user32.GetWindowTextW
            GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
            IsWindowVisible = ctypes.windll.user32.IsWindowVisible
             
            titles = []
            def foreach_window(hwnd, lParam):
                if IsWindowVisible(hwnd):
                    length = GetWindowTextLength(hwnd)
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    titles.append(buff.value)
                return True
            EnumWindows(EnumWindowsProc(foreach_window), 0)

            tab_count=0
            #print(tab_count)
            flag=0
            for i in titles:
                if i != '':
                    #print(i,tab_count)
                    i=i.split('-')
                    tab_count+=1
                    if(" Google Chrome" in i)|("Google Chrome" in i):
                        flag=1
                        break
                        
            if(flag==0):
            
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "chrome")
                self.open_path_function()
                return
                self.open_path.delete(0, 'end')

            else:
                user32 = ctypes.windll.user32
                user32.keybd_event(0x12, 0, 0, 0) #Alt
                time.sleep(0.1)
                user32.keybd_event(0x09, 0, 0, 0) #Tab
                user32.keybd_event(0x09, 0, 2, 0) #~Tab
                for i in range(tab_count-1):
                    user32.keybd_event(0x09, 0, 0, 0) #Tab
                    time.sleep(0.1)
                    user32.keybd_event(0x09, 0, 2, 0) #~Tab
                    
                user32.keybd_event(0x12, 0, 2, 0) #~Alt   
                time.sleep(0.1)
                keyboard.press_and_release('ctrl+t')
                keyboard.press_and_release('alt+d')
                pyperclip.copy(self.get_path[3:])
                keyboard.press_and_release('ctrl+v')
                keyboard.press_and_release('enter')                        
                self.open_path.delete(0, 'end')
            return
                
        elif("add:" in self.get_path):
            self.open_path.delete(0, 'end')
            self.get_path=self.get_path.split(' ')
            #print(self.get_path)
            if(self.get_path[1]=="file:"):
                self.askfile=1
                self.open_path.insert(0, "Please select a file")
            elif(self.get_path[1]=="folder:"):
                self.askfile=0
                self.open_path.insert(0, "Please select a folder")
            
            # Adding file to database
            database=dict()
            with open(self.database_file, 'r') as f:
                for row in f:
                    self.database.append(row)
                    if (row is not "\n"):
                        row = row.rstrip()
                        row = row.split(",")
                        database.update({row[0]: row[1]})
                f.close()
            if(self.get_path[2] not in database.keys()):
                self.create_path()
            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Path already exists!")
               
        else:
            database=dict()
            with open(self.database_file, 'r') as f:
                for row in f:
                    self.database.append(row)
                    if (row is not "\n"):
                        row = row.rstrip()
                        row = row.split(",")
                        database.update({row[0]: row[1]})
                f.close()
            if(self.get_path in database.keys()):
                self.open_path.delete(0, 'end')
                self.check_dir_path(database)
                #webbrowser.open(database[self.get_path])

            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Path does not exist!")
        
            
    def write_path_to_database(self,tempdir,path):
        f=open(self.database_file, 'a')
        f=open(self.database_file, 'a')
        f.write(path+","+tempdir+"\n")
        f.close()

    def create_path(self):
        root = tkinter.Tk()
        root.withdraw()  

        currdir = os.getcwd()
        if(self.askfile==0):
            tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        else:
            tempdir = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
        if len(tempdir) > 0:
            self.write_path_to_database(tempdir,self.get_path[2])
            self.open_path.delete(0, 'end')
        else:
            self.open_path.delete(0, 'end')
            self.open_path.insert(0, "Failed to add!")

    def dragwin(self,event):
        x = self.window.winfo_pointerx() - self._offsetx
        y = self.window.winfo_pointery() - self._offsety
        self.window.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y
        
    def hider(self,event=0):
        if(self.hide==1):
            self.window.attributes('-alpha', 1)
            self.hide=0
        else:
            self.window.attributes('-alpha', 0.3)
            self.hide=1

    def exit(self):
        self.window.destroy()
        
    def hide_entry(self):
        if(self.hide_entry_window==1):
            self.open_path=tkinter.ttk.Entry(self.Frame_0,font=self.large_font)
            self.open_path.pack(side=tkinter.RIGHT)
            self.hide_entry_window=0
            #print("Created!")
        else:
            self.open_path.destroy()
            self.hide_entry_window=1
            #print("destroyed")

    # Adding features for version 4.0
    
    def do_nothing(self):        
        pass


    def __init__(self):
        self.additional_args=0
        self.prev_args=[]
        self.check_macro=0
        self.get_path=None
        self.database=list()
        self.window=tkinter.Tk()
        self.window.title("Final AI")
        self._offsetx = 0
        self._offsety = 0
        self.hide=1
        self.askfile=0
        self.database_file="data/ai.txt"
        if(os.path.isfile(self.database_file)) is not True:
                f=open("data/ai.txt",'w+')
                f.close()
        self.macro_dict={}
        self.hide_entry_window=0
        self.large_font = ('Regular ',13)
        self.main_frame=tkinter.Frame(self.window)
        self.main_frame.pack(side=tkinter.TOP)
        self.Frame_0=tkinter.Frame(self.main_frame)
        self.Frame_0.pack(side=tkinter.TOP)
        self.Frame_1=tkinter.Frame(self.main_frame)
        self.Frame_1.pack(side=tkinter.LEFT)
        self.background_color={'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000', 'green': '#00FF00'}
        self.open_path=tkinter.ttk.Entry(self.Frame_0,font=self.large_font)
        self.open_path.pack(side=tkinter.RIGHT)
        
        '''
        photo=tkinter.PhotoImage("icons\0.png")
        self.home_button=tkinter.Button(self.Frame_0,image=photo,command=lambda: self.hide_entry())
        self.home_button.pack(side=tkinter.LEFT)
        '''
        
        self.window.bind('<Button-1>',self.clickwin)
        self.window.bind('<B1-Motion>',self.dragwin)
        self.window.bind('<Triple-Button-1>', self.hider)
        self.open_path['background']='#DCDCDC'

        self.window.bind("<Return>", lambda x: self.open_path_function())
        self.window.overrideredirect(True)
        #self.window.attributes('-alpha', 0.3)
        self.window.wm_attributes("-topmost", 1)
        self.window.mainloop()
        
p=FInal_AI()
