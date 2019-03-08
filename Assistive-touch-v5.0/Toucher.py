import tkinter
from tkinter import ttk
import os
import webbrowser
from tkinter.messagebox import *
import tkinter.filedialog
import pythoncom, pyHook
import _thread
import keyboard
import time
import ctypes
import pyperclip
from win32gui import GetWindowText, GetForegroundWindow
import imaplib
import datetime
import threading
from cryptography.fernet import Fernet
from settings import *
import auth_calendar as calendar
import subprocess


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
            if(nick_name == "pass"):
                continue
            nick_name = nick_name.replace(" ", "_")
            x = nick_name + " " + str(t[1])
            tv.insert('', 'end', values=(x))
        #help_window.bind("<Escape>",lambda: help_window.destroy())
        help_window.mainloop()

# check primary mail
    def check_mail(self):
        if(len(str((self.window.focus_get()))) > 5 ):
            self.window.after(300000, lambda: self.check_mail())
            return
        with open(self.login_database,'r') as f:
            lines = f.readlines()
            if(len(lines)==0):
                return
            f1 = str.encode(lines[0][2:-2])
            f1 = Fernet(f1)
            username = str((f1.decrypt((str.encode(lines[1][2:-2])))))[2:-1]
            password = str((f1.decrypt((str.encode(lines[2][2:-1])))))[2:-1]
            print(username,password)
        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        obj.login(username,password)
        obj.select()
        x = ((obj.uid('search', 'SINCE 1-May-2018 X-GM-RAW "label:unread category:primary "'))[1])
        self.unread_mail_count= x[0].decode("utf-8")
        self.current_mail_count = len(self.unread_mail_count.split(" "))
        if(self.unread_mail_count.split(" ")[0]==''):
            self.current_mail_count = 0
        if(self.current_mail_count > self.previous_mail_count):
            self.found_new_mail = 1
        else:
            self.found_new_mail = 0
        self.previous_mail_count = self.current_mail_count
        print(self.unread_mail_count)
        if(self.unread_mail_count!=''):
            self.unread_mail_count= 1
        else:
            self.unread_mail_count= 0
        obj.logout()
        #print(self.unread_mail_count,x[0].decode("utf-8"))

# Change button to add gmail logo
        if(self.hide_entry_window==0):  
            print("here")
            if(self.found_new_mail==1):
                self.home_button.configure(image = self.gmail_half)
                self.home_button.image=self.gmail_half
                self.open_path.delete(0,"end")
                self.open_path.insert(0,"Received new mail!")
                self.window.after(10000, lambda: self.hide_entry())
            else:
                self.home_button.configure(image = self.photo_large)
                self.home_button.image=self.photo_large    
        else:
            print("her1e")
            if(self.found_new_mail==1):
                self.hide_entry()   
                self.open_path.insert(0,"Received new mail!")
                self.window.after(10000, lambda: self.hide_entry())
                time
                self.home_button.configure(image = self.gmail)
                self.home_button.image=self.gmail
            else:
                self.home_button.configure(image = self.photo_full)
                self.home_button.image=self.photo_full
        self.window.update()   
        self.window.after(300000, lambda: self.check_mail())                 
        
    def check_dir_path(self):
        self.update_database_dict()
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
                flag=1
                break
        user32 = ctypes.windll.user32
        #print(self.database_dict[self.get_path])
        if(".exe" in self.database_dict[self.get_path]):
            subprocess.call("\""+str(self.database_dict[self.get_path])+"\"")
            return
        if(flag==0):
            os.system("start "+ str(self.database_dict[self.get_path]))
        else:
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
            pyperclip.copy(self.database_dict[self.get_path])
            keyboard.press_and_release('ctrl+v')
            keyboard.press_and_release('enter')                        
            self.open_path.delete(0, 'end')
        return  
        
    def exit_window(self):
        self.window.destroy()
        exit()
        
    def execute_admin_command(self):

# Lock the system
        if(self.prev_args=='lock'):
            self.open_path.delete(0,"end")
            self.open_path.insert(0,"Feature Disabled")

# Shutdown the sytem            
        if(self.prev_args=='shutdown'):
            self.open_path.delete(0,"end")
            self.open_path.insert(0,"Feature Disabled")
            #os.system("shutdown -s")      
            exit()

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
    
        if('pass' in database.keys()):
            self.open_path.delete(0, 'end')
            print("d= ",database['pass'])
            print("x=",self.open_path.get())
            if(database['pass']==self.get_path):
                self.open_path.insert(0,'Successfull!')
                self.execute_admin_command()
            else:
                self.open_path.insert(0,'Invalid Password!!')
        else:
            self.open_path.delete(0, 'end')
            self.open_path.insert(0,'Pls set pass first!!')
    
    def prev_args_list(self):    
        if(self.prev_args[0]=='set:'):
            with open(self.database_file, 'a') as f:
                f.write("pass"+","+self.open_path.get())
                
            self.open_path.delete(0, 'end')
            self.open_path.insert(0,'Successfull!')                
            self.open_path.configure(show='')
            return
        
        elif(self.prev_args=='lock')|(self.prev_args=='shutdown'):
            self.check_pass()
            self.open_path.configure(show='')
            return
        
    
    def open_path_function(self):
        self.update_database_dict()
        self.get_path=self.open_path.get()
        
        if(self.additional_args==1):
            self.additional_args=0
            self.prev_args_list()
            return
            

# Exit
        if(self.get_path=='exit'):
            self.exit_window()
            exit()

# Help            
        elif(self.get_path=='help'):
            self.show_window()
            
# Open settings GUI
        elif("settings" in self.get_path):
            self.open_path.delete(0, 'end')
            self.hide_entry()
            obj = settings()
            self.update_database_dict()
            
        try:
            res = eval(self.get_path)
            self.open_path.delete(0, 'end')            
            self.open_path.insert(0,res)
            return
        except:
            pass
      
# Macro      

        if('macro' in self.get_path):
            self.get_path=self.get_path.strip('macro: ')
            self.open_path.delete(0, 'end')
            if(self.get_path in self.macro_dict.keys()):
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, 'Key already present!')
            else:
                self.open_path.insert(0,'Recording Macro as: ' + str(self.get_path))
                self.open_path.configure(state="disabled")
                x=keyboard.record(until='escape', suppress=False, trigger_on_release=False)
                self.open_path.configure(state="normal")
                #print(type(x))
                self.macro_dict[self.get_path]=x
                #print(self.macro_dict,x) 
                self.open_path.delete(0, 'end')
                self.open_path.insert(0,'Macro-recorded as: ' + str(self.get_path))
            return
            
# Execute Macro
        elif("exe: " in self.get_path):
            self.get_path=self.get_path.split(' ')
            #print("the key is ", self.get_path[1])
            if(self.get_path[1] not in self.macro_dict.keys()):
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, 'Key does not exist!')
            else:
                self.open_path.delete(0, 'end')
                time.sleep(3)
                self.open_path.configure(state="disabled")
                keyboard.play(self.macro_dict[self.get_path[1]], speed_factor=1.0)
                self.open_path.configure(state="normal")
                self.open_path.insert(0, 'Macro \'{}\' Executed!'.format(self.get_path[1]))
            return


# Del commands 
           
        elif("del: " in self.get_path):
            self.get_path=self.get_path.split(' ')
            if(self.get_path[1] == "macro:"):
                if(self.get_path[2] not in self.macro_dict.keys()):
                    self.open_path.delete(0, 'end')
                    self.open_path.insert(0, 'Key does not exist!')
                else:
                    self.macro_dict.pop(self.get_path[2])
                    self.open_path.insert(0, 'Macro {} deleted'.format(self.open_path[1]))
                return
            elif(self.get_path[1] == "path:"):
                if(self.get_path[2]==""):
                    self.open_path.delete(0, 'end')
                    self.open_path.insert(0, 'No Key passed!')
                else:
                    self.delete_database_path()
                return
            
# Settings commands

        elif("set:" in self.get_path):
            self.get_path=self.get_path.split(' ')
            
# Settings - Color - Background
            if(self.get_path[1]=='color:'):
                try:
                    if(self.get_path[2].replace(" ",'')=='black'):
                        self.open_path['fg']="#00FF00"
                        self.open_path['background']=self.background_color[self.get_path[2].replace(" ",'')]
                        self.open_path.delete(0, 'end')
                    else:
                        self.open_path['background']=self.background_color[self.get_path[2].replace(" ",'')]
                        self.open_path.delete(0, 'end')
                except:
                    self.open_path.delete(0, 'end')
                    self.open_path.insert(0, "Invalid color option")
                    
# Settings - Color - Font 
            if(self.get_path[1]=='font:'):
                self.open_path['fg']=self.background_color[self.get_path[2].replace(" ",'')]
                
# Settings - Password                 
            elif('pass:' in self.get_path[1]):
                self.open_path.delete(0, 'end')
                self.open_path.configure(show='*')
                self.additional_args=1
                self.prev_args=self.get_path
                            
# If empty setting passed
            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Please pass -args")
            return
            
# Lock the system
        elif("lock" in self.get_path):
            self.open_path.delete(0, 'end')
            self.open_path.insert(0, "Enter Password:")
            self.open_path.configure(show='*')
            self.additional_args=1
            self.prev_args=self.get_path
            return
            
            
# Shutdown the system            
        elif("shutdown" in self.get_path):
            self.open_path.delete(0, 'end')
            self.open_path.configure(show='*')
            self.additional_args=1
            self.prev_args=self.get_path
            return

# Social Media links            
        elif(self.get_path in ["gmail","facebook","linkedin","youtube", "github", "google","reddit"]):
            self.get_path = str(self.get_path) + ".com"
            self.open_link()
            return

# Google Search
        elif("G:" in self.get_path):
            self.get_path = self.get_path[3:]
            self.open_link()
            return
                
# Adding file/folder to the database file
        elif("add:" in self.get_path):
            self.open_path.delete(0, 'end')
            self.get_path=self.get_path.split(' ')
            
            if(self.get_path[2] in self.keywords): 
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Keyword Error!")
                return
                
# Adding file
            if(self.get_path[1]=="file:"):
                self.askfile=1
                self.open_path.insert(0, "Please select a file")
             
# Adding Folder
            elif(self.get_path[1]=="folder:"):
                self.askfile=0
                self.open_path.insert(0, "Please select a folder")
            
            if(self.get_path[1] in ["file:", "folder:"]) & (self.get_path[2] not in self.database_dict.keys()):
                self.create_path()
            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Path already exists!")
               
        else:                
            if(self.get_path in self.database_dict.keys()):
                self.open_path.delete(0, 'end')
                self.update_database_dict()
                self.check_dir_path()
                return
            else:
                self.open_path.delete(0, 'end')
                self.open_path.insert(0, "Unknown cmd!")
                return
        return

# Updating the self.database_dict
    def update_database_dict(self):
        self.database_dict=dict()
        with open(self.database_file, 'r') as f:
            for row in f:
                self.database.append(row)
                if (row is not "\n"):
                    row = row.rstrip()
                    row = row.split(",")
                    if(len(row)<3):
                        self.database_dict.update({row[0]: row[1]})
            f.close()
                
# Delete a path from the database
    def delete_database_path(self):
        f = open(self.database_file, 'r')
        lines = f.readlines()
        f.close
        f = open(self.database_file, 'w')
        for line in lines:
            line = line.split(",")
            if(line[0]==self.get_path[2]):
                continue
            else:
                f.write(str(line[0]) +","+str(line[1]))
        self.update_database_dict()
        f.close()
        
# Open links
    def open_link(self):
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
        for i in titles:
            if i != '':
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
            for i in range(tab_count-2):
                user32.keybd_event(0x09, 0, 0, 0) #Tab
                time.sleep(0.1)
                user32.keybd_event(0x09, 0, 2, 0) #~Tab
                
            user32.keybd_event(0x12, 0, 2, 0) #~Alt   
            time.sleep(0.1)
            active_window=GetWindowText(GetForegroundWindow())
            #print(active_window,type(active_window))
            keyboard.press_and_release('ctrl+t')
            keyboard.press_and_release('alt+d')
            pyperclip.copy(self.get_path)
            keyboard.press_and_release('ctrl+v')
            keyboard.press_and_release('enter')                        
            self.open_path.delete(0, 'end')
        return

            
    def write_path_to_database(self,tempdir,path):
        f=open(self.database_file, 'a')
        f.write(path+","+tempdir+"\n")       
        self.update_database_dict()        
        f.close()

    def create_path(self):
        root = tkinter.Tk()
        root.withdraw()  

        currdir = os.getcwd()
        if(self.askfile==0):
            tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        elif(self.askfile==1):
            tempdir = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
        else: 
            tempdir=self.get_path[3]
        if len(tempdir) > 0:
            self.write_path_to_database(tempdir,self.get_path[2])
            self.open_path.delete(0, 'end')
            self.open_path.insert(0, str(self.get_path[2])+" added")
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
        try:
            self.open_path.delete(0, 'end')
        except:
            pass
        if(self.hide_entry_window==1): 
            self.hide_entry_window=0
            sv = tkinter.StringVar()
            sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))
            
# Entry in hide function
            self.open_path=tkinter.Entry(self.Frame_0,font=self.large_font,bg="#101010",fg="#00FF00",bd=1,width=1,insertbackground="#00FF00",textvariable=sv)
            self.open_path.pack(side=tkinter.RIGHT)
            
            self.open_path.bind("<Return>", lambda x: self.open_path_function())        
            self.open_path.bind('<Down>', lambda x: self.downkey())
            
            self.open_path.bind('<Up>', lambda x: self.upkey())
            self.open_path.focus()
            self.open_path.config(highlightbackground="#8B0000")


            
            for i in range (1,20):
                try:
                    self.open_path["width"]=i
                    self.window.update()
                except:
                    pass
                if(i==10):
                    if(self.unread_mail_count>0):
                        self.home_button.configure(image = self.gmail_half)
                        self.home_button.image=self.gmail_half
                    else:
                        self.home_button.configure(image = self.photo_large)
                        self.home_button.image=self.photo_large  
                self.window.update()
                time.sleep(0.003)
                  
        else:
            self.listbox.destroy()
            for i in range (1,21):
                self.open_path["width"]=20-i
                self.window.update()
                time.sleep(0.003)
            
            self.open_path.destroy()
            self.list_box_present = 0
            self.hide_entry_window=1
            if(self.unread_mail_count>0):
                self.home_button.configure(image = self.gmail)
                self.home_button.image=self.gmail
            else:
                self.home_button.configure(image = self.photo_full)
                self.home_button.image=self.photo_full
            self.window.update()


    # Adding features for version 4.0
    
    def do_nothing(self):        
        pass
        
    def callback(self,sv):
        path = sv.get()

        insert = 0
        if self.open_path.get() != '':
            if (self.list_box_present == 0):
                self.Frame_1=tkinter.Frame(self.main_frame)
                self.Frame_1.pack(side=tkinter.RIGHT)            
                self.listbox = tkinter.Listbox(self.Frame_1,width=19,height=2,bd=0,bg='black',fg='#00FF00',font=self.large_font)
                self.listbox.bind('<Return>', lambda x: self.enterkey())
                self.listbox.bind("<Escape>", lambda x: self.open_path.focus())
                self.listbox.pack(side="bottom",fill="both", expand=True)
                self.listbox.config(highlightbackground="#8B0000")
                self.list_box_present = 1            
            self.listbox.delete(0,tkinter.END)
        else:
            self.listbox.destroy()
            self.Frame_1.destroy()
            self.window.update()
            self.list_box_present = 0 
        
        if(path!=''):
            all = list(self.database_dict.keys()) + self.keywords
            temp=[]
            for i in all:
                if(path.lower()==str(i[0:len(path)]).lower()):
                    temp.append(i)
                self.listbox['height'] = len(temp)
                #print(temp)
            for i in temp: 
                self.listbox.insert(tkinter.END, i)
                insert = 1
            if (insert == 0):
                self.listbox.destroy()
                self.Frame_1.destroy()
                self.window.update()
                self.list_box_present = 0 
    
# Update calendar()
    def update_calendar(self):
        try:
            res = calendar.main()
            self.window.after(1800000, lambda: self.check_mail())
            #print(res)
            f = open("data/calendar.txt","w+")
            for i in res:
                f.write(str(i)+'\n')
            f.close()
        except:
            return
    
    def notify_calendar(self):
        x=(self.window.focus_get())
        if(x!=None):
            self.window.after(10000, lambda: self.notify_calendar())                            
            return         
        line = self.events[0]
        self.events = self.events[1:]         
        if(self.hide_entry_window==0):
            try:
                self.open_path.delete(0,'END')
            except:
                pass
            self.open_path.insert(0,line.split(",")[1][2:-3])
        else:
            self.hide_entry()
            self.open_path.insert(0,line.split(",")[1][2:-3])
        #print(self.events)
    def check_calendar(self):
        with open("data/calendar.txt",'r') as f:
            lines = f.readlines()
            now = str(datetime.datetime.now()).split(" ")
            for line in lines:
                #print(now[0],line[2:12],line[13:18])
                if(line[2:12]==now[0]):
                    event_time = line[13:18]
                    current_time = now[1][:5]
                    #print(event_time,current_time)
                    if(int(event_time[:2]) - int(current_time[:2]) == 1):
                        print("here")
                        event_time = int(event_time[:2])*100 + int(event_time[3:])
                        current_time = int(current_time[:2])*100 + int(current_time[3:])
                        current_time = current_time + 100
                        if(current_time<2400):
                            z = current_time - event_time 
                            event_starts = (60- z)*60*1000 
                            self.events.append(line)
                            if(event_starts<720000):
                                event_starts = 10000
                            else:
                                event_starts = event_starts - 720000                            
                            self.window.after(event_starts, lambda: self.notify_calendar())        
                event_time = line[13:18]
                current_time = now[1][:5]   
                if(int(event_time[:2]) - int(current_time[:2]) < 1):
                    if((int(event_time[:2])*100==int(current_time[:2])*100)&(int(event_time[3:])>int(current_time[3:]))):
                        event_starts = (int(event_time[3:])-int(current_time[3:]))*60*1000
                        if(event_starts<720000):
                            event_starts = 10000
                        else:
                            event_starts = event_starts - 720000
                        self.events.append(line)
                        self.window.after(event_starts, lambda: self.notify_calendar())                            
    def downkey(self):
        self.listbox.focus()
        
    def upkey(self):
        self.listbox.focus()

    def enterkey(self):
        selected = self.listbox.get(tkinter.ACTIVE)
        self.open_path.delete(0, tkinter.END)
        self.open_path.insert(0, selected)
        self.open_path_function()
        
    def __init__(self,full=0):
        if(full!=1):
            exit()
        self.additional_args=0
        self.prev_args=[]
        self.check_macro=0
        self.get_path=None
        self.login_database='data/login.txt'
        self.database=list()
        self.database_dict={}
        self.window=tkinter.Tk()
        self.window.title("Final AI")
        self._offsetx = 0
        self._offsety = 0
        self.hide=1
        self.current_mail_count = 0
        self.previous_mail_count = 0
        self.found_new_mail = 0
        self.list_box_present = 0
        self.askfile=0
        self.events=[]
        self.unread_mail_count=0
        self.database_file="data/database.txt"
        self.macro_dict={}
        self.hide_entry_window=1
        self.large_font = ('Verdana',12)
        self.main_frame=tkinter.Frame(self.window)
        self.main_frame.pack(side=tkinter.TOP)
        self.Frame_0=tkinter.Frame(self.main_frame)
        self.Frame_0.pack(side=tkinter.TOP)
        self.Frame_1=tkinter.Frame(self.main_frame)
        self.Frame_1.pack(side=tkinter.RIGHT)
        predifined_user_files = ["Documents","Downloads","Pictures","Music","Videos"]
        predefined_apps = ["control","settings","calc","cmd"]
        
# icons
        self.photo_large = tkinter.PhotoImage(file = "icons/d5.png")
        self.photo_full = tkinter.PhotoImage(file = "icons/d3.png")  
        self.gmail = tkinter.PhotoImage(file = "icons/d1.png")
        self.gmail_half= tkinter.PhotoImage(file = "icons/d2.png")        
        
        
# Check for the database file and update the database.txt
        if(os.path.isfile(self.database_file)) is not True:
                f=open("data/database.txt",'w+')
                lines = f.readlines()
                if(len(lines)==0):
                    current_user = os.getlogin()
                    for i in predifined_user_files:
                        f.write(i.lower()+","+"c:\\Users\\"+current_user+"\\"+i+"\n")
                    for i in predefined_apps:
                        f.write(i+","+"c:\\Windows\\system32\\"+i+".exe"+"\n")
                f.close()
        self.update_database_dict()

# Values
        self.background_color={'black': '#101010', 'white': '#FFFFFF', 'red': '#FF0000', 'green': '#00FF00'}
        self.keywords=["exit","add","macro","exe","gmail","github","linkedin","shutdown","lock","facebook","help"]
                
        sv = tkinter.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.callback(sv))

# Entry        
        self.open_path=tkinter.Entry(self.Frame_1,font=self.large_font,width=20,textvariable=sv) 
        self.open_path["bg"] = "#101010"
        self.open_path["fg"] = "#00FF00"
        self.open_path["insertbackground"] = "#00FF00" 


        
# Button        
        photo=tkinter.PhotoImage(file = "icons/d.png")
        
        self.home_button=tkinter.Button(self.Frame_0,image=photo,width=53,height=50,command=lambda: self.hide_entry())
        self.home_button["bd"] = 0
        self.home_button.pack(side=tkinter.LEFT)

# Listbox        
        self.listbox = tkinter.Listbox(self.Frame_1,width=20,height=4,bg='black',fg="white",font=10)
        
# Window Configurations
        self.Frame_0['background']='white'
        self.Frame_1['background']='white'
        self.Frame_1['height']=2
        self.main_frame['background']='white'
        
        self.home_button.bind('<Button-1>',self.clickwin)
        self.home_button.bind('<B1-Motion>',self.dragwin)
        self.home_button.bind('<Triple-Button-1>', self.do_nothing())
        self.home_button.bind('<Double-Button-1>', self.do_nothing())
        
# Update calendar
        self.update_calendar()
        self.check_calendar()
        self.window.after(1800000, lambda: self.check_mail())
#self.window.bind("<Return>", lambda x: self.open_path_function())
        self.window.wm_attributes("-transparentcolor", "white")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", 1)
        
        self.window.after(300000, lambda: self.check_mail())        
        self.window.mainloop()
        
        
        
        
p=FInal_AI(1)

