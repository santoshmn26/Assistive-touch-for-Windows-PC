from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import tkinter.filedialog 
from tkinter import messagebox
from cryptography.fernet import Fernet
import auth_calendar as calendar
import webbrowser
import json



class settings:
    def get_radiobutton(self,v):
        if(v==2):
            self.file_entry.delete(0,"end")        
            self.file_browse.configure(state=tk.DISABLED)
            self.file_entry.configure(state=tk.DISABLED)
            self.folder_browse.configure(state=tk.NORMAL)
            self.folder_entry.configure(state=tk.NORMAL)
            self.file_folder=0
        else:
            self.file_browse.configure(state=tk.NORMAL)
            self.file_entry.configure(state=tk.NORMAL)
            self.folder_entry.delete(0,"end")
            self.folder_browse.configure(state=tk.DISABLED)
            self.folder_entry.configure(state=tk.DISABLED)            
            self.file_folder=1
        
# Exit
    def cancel(self):
        self.settings_window_active=0
        self.root.destroy()

# Add new file
    def add_path(self,v):
        root = tk.Tk()
        root.withdraw()  

        currdir = os.getcwd()
        if((v==2)):
            tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        elif((v==1)):
            tempdir = tkinter.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a file')
        if len(tempdir) > 0:
            if((v==1)):
                self.file_entry.insert(tk.END, tempdir)
            else:
                self.folder_entry.insert(tk.END, tempdir)


    def update_database_dict(self):
        self.database_dict=dict()
        with open(self.database_file, 'r') as f:
            for row in f:
                if (row is not "\n"):
                    row = row.rstrip()
                    row = row.split(",")
                    if(len(row)<3)&(row[0]!='pass'):
                        self.database_dict.update({row[0]: row[1]})
        #print(self.database_dict.keys())
        
# Write to database            
    def write_to_database(self):
        #print(self.database_dict.keys(),self.name_entry.get())
        if(self.name_entry.get()!=''):
            for key in self.database_dict.keys():
                if key == self.name_entry.get():
                    messagebox.showinfo("Assistive-touch-path", "Name already exists")
                    return
            if(self.file_folder==1):
                if (self.file_entry.get()!=''):
                    with open(self.database_file, 'a') as f:
                        f.write(self.name_entry.get()+","+self.file_entry.get()+"\n")
                        messagebox.showinfo("Assistive-touch-path", "Successfull")
                else:
                        messagebox.showinfo("Assistive-touch-path", "Please provide a path for the shortcut")                    
            elif(self.file_folder==0):
                if(self.folder_entry.get()!=''):
                    with open(self.database_file, 'a') as f:
                    #print(self.folder_entry.get())
                        f.write(self.name_entry.get()+","+self.folder_entry.get()+"\n")
                        messagebox.showinfo("Assistive-touch-path", "Successfull")
                else:
                        messagebox.showinfo("Assistive-touch-path", "Please provide a path for the shortcut")                    

            
            self.update_database_dict()
        else:
            messagebox.showinfo("Assistive-touch-path", "Please provide a New Name for the shortcut")
            
# save mail info    
    def mail_save(self):
        if(self.username_entry.get()=='') | (self.password_entry.get()==''):
            messagebox.showinfo("Assistive-touch-path", "Please provide Username and Password")
        else:
            f1 = Fernet(self.key)
            with open(self.login_database, 'w') as f:
                f.write(str(self.key)+"\n"+str(f1.encrypt(self.username_entry.get().encode()))+"\n"+str(f1.encrypt(self.password_entry.get().encode())))
            messagebox.showinfo("Assistive-touch-path", "Saved Credentials")
    
    def calendar(self):
        #calendar.main()
        try:
            calendar.main()
        except:
            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open("https://developers.google.com/calendar/quickstart/python?refresh=1")
        
    def save_cred(self):
            id = self.client_id_entry.get()
            secret = self.client_secret_entry.get()
            if(id!='')&(secret!=''):
                with open ("data/credentials.json",'r+') as f:
                    data = json.load(f)
                    data['installed']["client_secret"] = secret
                    data['installed']["client_id"] = id
                    f.seek(0)
                    json.dump(data, f, indent=4)          
            
    def check_creds(self):
        try:
            with open ("data/credentials.json",'r') as f:
                    data = json.load(f)
                    secret = data['installed']["client_secret"] 
                    id = data['installed']["client_id"]
                    self.client_id_entry.insert(0,id)
                    self.client_secret_entry.insert(0,secret)
        except:
            return
        
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ttk.Notebook")
        self.key = Fernet.generate_key()
        nb = ttk.Notebook(self.root)
        self.file_folder=0
        page1 = ttk.Frame(nb)
        main_frame = ttk.Frame(page1)
        main_frame.pack(side = tk.TOP, anchor=tk.CENTER)
        self.database_dict = dict()
        self.database_file = "data/database.txt"
        self.login_database = "data/login.txt"
        self.settings_window_active=1
        frame0 = ttk.Frame(main_frame)
        frame1 = ttk.Frame(main_frame)
        frame2 = ttk.Frame(main_frame)
        frame3 = ttk.Frame(main_frame)
        frame4 = ttk.Frame(main_frame)
        frame5 = ttk.Frame(main_frame)


        frame0.pack(side=tk.TOP)
        frame1.pack(side=tk.TOP)
        frame2.pack(side=tk.TOP)
        frame3.pack(side=tk.TOP)
        frame4.pack(side=tk.TOP)
        frame5.pack(side=tk.TOP)

        self.v = tk.IntVar()
        file_button=ttk.Radiobutton(frame0, text="File",variable = self.v, value=1, command = lambda: self.get_radiobutton(1))
        file_button.pack(side=tk.LEFT,anchor=tk.W, padx=10, pady=5)
        folder_button=ttk.Radiobutton(frame0, text="Folder", variable = self.v, value=2, command = lambda: self.get_radiobutton(2))
        folder_button.pack(side=tk.LEFT,anchor=tk.W, padx=10, pady=5)
        
        
        path_Name = tk.Label(frame1,text='Name:        ')
        self.name_entry = ttk.Entry(frame1,width = 35)    
        dummy_space = tk.Label(frame1,text='                        ')
         
        add_file = tk.Label(frame2,text='Add File:       ')
        self.file_entry = ttk.Entry(frame2,width = 35)
        dummy_space_file = tk.Label(frame2,text='  ')
        
        add_folder = tk.Label(frame3,text='Add Folder   ')
        self.folder_entry = ttk.Entry(frame3,width = 35)
        dummy_space_folder = tk.Label(frame3,text='  ')
        
        
        self.file_browse = ttk.Button(frame2,text = "Browse",command = lambda: self.add_path(1))
        self.folder_browse = ttk.Button(frame3,text = "Browse", command = lambda: self.add_path(2))
            
        ok = ttk.Button(frame4,text = "  Ok  ",command = lambda: self.write_to_database())
        cancel = ttk.Button(frame4,text = "Cancel ",command = lambda: self.cancel())
        self.root.bind("<Escape>", lambda x: self.cancel())
        

        add_file.pack(side=tk.LEFT,anchor=tk.W)
        add_folder.pack(side=tk.LEFT,anchor=tk.W)


        self.file_entry.pack(side=tk.LEFT)
        dummy_space_file.pack(side=tk.LEFT)
        self.folder_entry.pack(side=tk.LEFT)
        dummy_space_folder.pack(side=tk.LEFT)
        
        
        path_Name.pack(side=tk.LEFT,anchor=tk.CENTER)
        self.name_entry.pack(side=tk.LEFT)
        
        self.file_browse.pack(side=tk.LEFT,anchor=tk.E)
        self.folder_browse.pack(side=tk.LEFT,anchor=tk.W)
        dummy_space.pack(side=tk.LEFT)
        
        
        
        ok.pack(side=tk.LEFT,padx=10, pady=10)
        cancel.pack(side=tk.LEFT,padx=10, pady=10)
        page1.bind("<Return>",lambda x: self.write_to_database())
        
        # second page
        page2 = ttk.Frame(nb)
        page2_main_frame = ttk.Frame(page2)
        page2_main_frame.pack(side = tk.TOP)
        
        frame0 = ttk.Frame(page2_main_frame)
        frame1 = ttk.Frame(page2_main_frame)
        frame2 = ttk.Frame(page2_main_frame)
        frame0.pack(side=tk.TOP)
        frame1.pack(side=tk.TOP)
        frame2.pack(side=tk.TOP)
        
        username = tk.Label(frame0, text = "Email-id:   ")
        password = tk.Label(frame1, text = "Password: ")
        
        self.username_entry = tk.Entry(frame0, width =35)
        self.password_entry = tk.Entry(frame1, width =35,show='*')
        
        #self.test = ttk.Button(frame2, text = "Test")
        self.save = ttk.Button(frame2, text = "Save", command = lambda: self.mail_save())
        
        username.pack(side=tk.LEFT,padx=10,pady=20)
        self.username_entry.pack(side=tk.LEFT,padx=10,pady=20)
        password.pack(side=tk.LEFT,padx=10,pady=5)
        self.password_entry.pack(side=tk.LEFT,padx=10,pady=5)
        #self.test.pack(side=tk.LEFT,padx=10,pady=10)
        self.save.pack(side=tk.LEFT,padx=10,pady=10)
        
        page2.bind("<Return>",lambda x: self.mail_save())
        
        
        page3 = ttk.Frame(nb)
        

        
        page4 = ttk.Frame(nb)
        page5 = ttk.Frame(nb)
        main_frame3=ttk.Frame(page4)
        main_frame3.pack(side=tk.TOP)
        frame03 = ttk.Frame(main_frame3)
        frame13 = ttk.Frame(main_frame3)
        frame23 = ttk.Frame(main_frame3)

        frame03.pack(side=tk.TOP)
        frame13.pack(side=tk.TOP)
        frame23.pack(side=tk.TOP)
        
        frame41 = ttk.Frame(page5)
        frame42 = ttk.Frame(page5)
        frame43 = ttk.Frame(page5)
        frame44 = ttk.Frame(page5)
        frame41.pack(side=tk.TOP,anchor=tk.W)
        frame42.pack(side=tk.TOP,anchor=tk.W)
        frame43.pack(side=tk.TOP,anchor=tk.W)
        frame44.pack(side=tk.LEFT,anchor=tk.W)
        
        a = tk.Label(frame03, text="Product: Assistive-touch")
        a.pack(side=tk.LEFT,anchor=tk.NW)
        tk.Label(page4,text = "Version: V4.5(Beta)").pack(side=tk.TOP,anchor=tk.W)
        tk.Label(page4,text = "Created-By: Santosh Muniswamygowda Nagaraja").pack(side=tk.TOP,anchor=tk.W)
        tk.Label(page4,text = "Source-Files: https://github.com/santoshmn26/Assistive-touch-for-Windows-PC").pack(side=tk.TOP,anchor=tk.W)
        tk.Label(page4,text = "Report-Bugs: https://github.com/santoshmn26/Assistive-touch-for-Windows-PC/issues").pack(side=tk.TOP,anchor=tk.W)
        
        tk.Label(frame41, text = "Authorize Assitive touch to access your Gmail Calendar API").pack(side = tk.LEFT, anchor =tk.W,padx=5,pady=5)
        
        tk.Label(frame42, text = "Client-ID").pack(side = tk.LEFT, anchor =tk.W,padx=5,pady=5)
        self.client_id_entry = tk.Entry(frame42, width = 35,show='*')
        self.client_id_entry.pack(padx=29,pady=5)
        
        tk.Label(frame43, text = "Client Secret").pack(side = tk.LEFT, anchor =tk.W,padx=5,pady=5)
        self.client_secret_entry = tk.Entry(frame43, width =35,show='*')
        self.client_secret_entry.pack(padx=10,pady=5)
        
        tk.Label(frame44, text = "                             ").pack(side = tk.LEFT, anchor =tk.W,padx=5,pady=5)
        self.get_keys = ttk.Button(frame41, text = "Get Client Keys", command = lambda: self.calendar())
        self.get_keys.pack(padx=10,pady=5)
        self.cred_save = ttk.Button(frame44, text = "Save Credentials", command = lambda: self.save_cred())
        self.cred_save.pack(side = tk.LEFT,anchor =tk.CENTER,padx=10,pady=3)
        self.authorize = ttk.Button(frame44, text = "Authorize", command = lambda: self.calendar())
        self.authorize.pack(side = tk.LEFT,anchor =tk.CENTER,padx=10,pady=3)
        self.check_creds()

        nb.add(page1, text='Add File/Folder')
        nb.add(page2, text='Gmail')
        nb.add(page5, text="Calendar")       
        nb.add(page3, text='Settings')
        nb.add(page4, text='About')

        
# Default radio button
        self.v.set(1)
        self.get_radiobutton(1)   
        self.update_database_dict()        
        
        self.root.geometry('470x180')
        nb.pack(expand=1, fill="both")

        self.root.mainloop()
