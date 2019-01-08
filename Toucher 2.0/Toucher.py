import tkinter
import os
import webbrowser
from tkinter.messagebox import *
from tkinter import ttk
import tkinter.filedialog

class FInal_AI:
    def show_window(self):
        help_window = tkinter.Tk()
        f = open("C:/Users/santo/OneDrive/Documents/Python Scripts/ai.txt", 'r')
        tv = ttk.Treeview(help_window)
        tv['columns'] = ('Nick Name', 'File path')
        tv.heading('Nick Name', text='Nick Name')
        tv.column('Nick Name', anchor='w', width=100)
        tv.heading('File path', text='File path')
        tv.column('File path', width=200, anchor='w')


        #####################
        tv['show'] = 'headings'  # important piece of code removes the unwanted first column
        #####################

        tv.grid(row=0)
        for row in f:
            t = row.split(",")
            nick_name = t[0]
            nick_name = nick_name.replace(" ", "_")
            x = nick_name + " " + str(t[1])
            tv.insert('', 'end', values=(x))
        help_window.mainloop()

    def exit_window(self):
        self.window.destroy()
    
    def do_nothing():
        pass

    def open_path_function(self):
        #print("was here")
        self.get_path=self.open_path.get()

        if(self.get_path=='exit'):
            self.exit_window()
            exit()
        elif(self.get_path=='help'):
            self.show_window()
        elif(self.get_path=='macro'):
            self.Rec_Button=tkinter.Button(self.window,text="REC.", command=self.do_nothing)
            self.Rec_Button.pack(side=tkinter.RIGHT)
            return
        elif(self.get_path=="exit macro"):
            self.Rec_Button.destroy()
            return
        elif("set:" in self.get_path):
            #print("Here")
            self.get_path=self.get_path.strip('set: ')
            if("file:" in self.get_path):
                self.get_path=self.get_path.strip('file: ')
                print(self.get_path)
                if("1" in self.get_path):
                    self.askfile=1
                    self.open_path.insert(0, "Option set to open file")
                elif("0" in self.get_path):
                    self.askfile=0
                    self.open_path.insert(0, "Option set to open Folder")
    
            #self.open_path.delete(0, 'end')
            return
            

        database=dict()
        with open("C:/Users/santo/OneDrive/Documents/Python Scripts/ai.txt", 'r') as f:
            for row in f:
                self.database.append(row)
                if (row is not "\n"):
                    row = row.rstrip()
                    row = row.split(",")
                    database.update({row[0]: row[1]})
            f.close()
        try:
            #print(type(database[self.get_path]))
            #print(self.get_path, database[self.get_path])
            #print("start "  + database[self.get_path])

            webbrowser.open(database[self.get_path])
            self.open_path.delete(0, 'end')
        except:
            self.create_path()
            
    def write_path_to_database(self,tempdir):
        f=open("C:/Users/santo/OneDrive/Documents/Python Scripts/ai.txt", 'a')
        f.write(self.get_path+","+tempdir+"\n")
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
            self.write_path_to_database(tempdir)
            self.open_path.delete(0, 'end')
        else:
            print("failed to add")

    def dragwin(self,event):
        x = self.window.winfo_pointerx() - self._offsetx
        y = self.window.winfo_pointery() - self._offsety
        self.window.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x
        self._offsety = event.y
    def hider(self,event):
        if(self.hide==1):
            self.window.attributes('-alpha', 1)
            self.hide=0
        else:
            self.window.attributes('-alpha', 0.3)
            self.hide=1

    def exit(self):
        self.window.destroy()

    def do_nothing(self):
        
        pass
        

    def __init__(self):
        self.get_path=None
        self.database=list()
        self.window=tkinter.Tk()
        self.window.title("Final AI")
        self._offsetx = 0
        self._offsety = 0
        self.hide=1
        self.askfile=0
        
        self.large_font = ('Verdana',13)
        self.Frame_0=tkinter.Frame(self.window)
        self.Frame_0.pack(side=tkinter.LEFT)
        
        self.open_path=tkinter.Entry(self.Frame_0,fg='#7CFC00',font=self.large_font)
        self.open_path.pack(side=tkinter.RIGHT)
        
        #self.text_suggestions=tkinter.Text(self.Frame_0,height=10,width=27)
        #self.text_suggestions.pack(side=tkinter.BOTTOM)
        #Bg=tkinter.PhotoImage(file="C:\\Users\\santo\\Downloads\\no_bg.png")
        #photo=tkinter.PhotoImage(file="C:\\Users\\santo\\Downloads\\Backup files\\Scripts\\Toucher\\apple.jpg")
        
        
        self.window.bind('<Button-1>',self.clickwin)
        self.window.bind('<B1-Motion>',self.dragwin)
        self.window.bind('<Triple-Button-1>', self.hider)
        self.open_path['background']='#000000'

        self.window.bind("<Return>", lambda x: self.open_path_function())
        self.window.overrideredirect(True)
        self.window.attributes('-alpha', 0.3)
        self.window.wm_attributes("-topmost", 1)
        self.window.mainloop()
p=FInal_AI()
