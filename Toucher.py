import tkinter
import os
import webbrowser
from tkinter.messagebox import *
from tkinter import ttk
import tkinter.filedialog

class FInal_AI:
    def show_window(self):
        help_window = tkinter.Tk()
        f = open("D:\Bro code\FInal AI.txt", 'r')
        i = 1
        tv = ttk.Treeview(help_window)
        tv['columns'] = ('Nick Name', 'File path', 'Number')
        tv.heading('Nick Name', text='Nick Name')
        tv.column('Nick Name', anchor='w', width=100)
        tv.heading('File path', text='File path')
        tv.column('File path', width=150, anchor='w')
        tv.heading('Number', text='File path')
        tv.column('Number', width=150, anchor='w')

        #####################
        tv['show'] = 'headings'  # important piece of code removes the unwanted first column
        #####################

        tv.grid(row=0)
        for row in f:
            t = row.split(",")
            nick_name = t[0]
            nick_name = nick_name.replace(" ", "_")
            x = str(i) + " " + nick_name + " " + str(t[1])
            tv.insert('', 'end', values=(x))
            i += 1
        help_window.mainloop()

    def exit_window(self):
        self.window.destroy()

    def open_path_function(self):
        self.get_path=self.open_path.get()

        if(self.get_path=='exit'):
            self.exit_window()
            exit()
        elif(self.get_path=='help'):
            self.show_window()

        database=dict()
        with open("D:\Bro code\FInal AI.txt", 'r') as f:
            for row in f:
                self.database.append(row)
                if (row is not "\n"):
                    row = row.rstrip()
                    row = row.split(",")
                    database.update({row[0]: row[1]})
            f.close()
        try:
            print(type(database[self.get_path]))
            print(self.get_path, database[self.get_path])
            print("start "  + database[self.get_path])
            webbrowser.open(database[self.get_path])
        except:
            self.create_path()
    def write_path_to_database(self,tempdir):
        f=open("D:\Bro code\FInal AI.txt", 'a')
        f.write(self.get_path+","+tempdir+"\n")
        f.close()

    def create_path(self):
        root = tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        currdir = os.getcwd()
        tempdir = tkinter.filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
        if len(tempdir) > 0:
            print("You chose", tempdir)
            self.write_path_to_database(tempdir)
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
        self.window.overrideredirect(True)
        self._offsetx = 0
        self._offsety = 0
        self.hide=1
        self.window.bind('<Button-1>',self.clickwin)
        self.window.bind('<B1-Motion>',self.dragwin)
        self.window.bind('<Double-Button-1>', self.hider)
        self.open_path=tkinter.Entry()
        self.open_path.pack(side=tkinter.LEFT)
        self.window.bind("<Return>", lambda x: self.open_path_function())
        self.window.overrideredirect(True)
        self.window.attributes('-alpha', 0.3)
        self.window.wm_attributes("-topmost", 1)
        self.window.mainloop()
p=FInal_AI()
