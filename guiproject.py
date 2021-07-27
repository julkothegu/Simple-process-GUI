from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import psutil
import sys
import time
import ctypes
from ctypes import wintypes
from win32 import win32gui as g_

root = tk.Tk()

height = 800
width = 900

listbox_info = {}
listbox_info2 = {}
process_list = []
cur_selections = []
cur_running = []
process_names = set()

user32 = ctypes.windll.user32

class processes(object):
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid
        self.time_spent = 0

def cur_process():
    for x in process_list:
        if psutil.pid_exists(x.pid):
            p = psutil.Process(x.pid)
            if p in psutil.process_iter():
                if p.status() == psutil.STATUS_RUNNING:
                    name = x.name
                    pid = x.pid
                    loop(name, pid, x)
                    x.time_spent = time.perf_counter()

    root.after(1000, cur_process)

def loop(namex, pidx, x):
    start_time = time.time()
    t = 0

    #While the process is running, check if foreground window (window currently being used) is the same as the process

    h_wnd = user32.GetForegroundWindow()
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(h_wnd, ctypes.byref(pid))
    p = psutil.Process(pid.value)

    name = str(p.name())
    name2 = str(namex)

    if name2 == name:
        t = time.time() - start_time

    #Log the total time the user spent using the window
    x.time_spent += t

def find_procname(name):
    for p in psutil.process_iter(attrs=['pid','name']):
        if name in p.info['name']:
            return p.pid

def get_processes():
    for x in process_list:
        print(x.name, x.pid)

def add_process():
    for c in cur_selections:
        listbox_info2[c] = Lb.get(c)
        name = listbox_info2[c]
        pid = find_procname(name)
        process = create_process(name,pid)
        process_list.append(process)
        cur_selections.remove(c)

    create_listbox2(name, pid)
    del_selections()

def create_process(info, pid):
    return processes(info, pid)

def del_selections():
    for s in Lb.curselection():
        Lb.delete(s)

def display_time():
    for s in Lb2.curselection():
        for e in process_list:
            if Lb2.get(s) == e.name:
                print(e.time_spent)

canvas = tk.Canvas(root, height=height, width=width)
canvas.pack()

background_image = ImageTk.PhotoImage(Image.open('landscape.jpg'))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

button = tk.Button(root, text='Press me', bg='yellow', fg='red', command = lambda:[add_process()])
button.place(relx=0.6, rely=0.8, relwidth=0.25, relheight=0.25)

button2 = button = tk.Button(root, text='How much time have I spent?', bg='yellow', fg='blue', command = lambda:[display_time()])
button.place(relx=0.1, rely=0.8, relwidth=0.25, relheight=0.25)

def selecta(e):

    #Add the selected items to the cur_selections so they get added if you press the button
    if len(Lb.curselection()) > len(cur_selections):
        for y in Lb.curselection():
            if y not in cur_selections:
                cur_selections.append(y)
    # Make sure that if you deselect something it gets deleted from from cur_selections
    else:
        for i in cur_selections:
            if i not in Lb.curselection():
                cur_selections.remove(i)

def selecta2(e):
    pass

def create_listbox():
    for idx, proc in enumerate(psutil.process_iter(attrs=['pid', 'name', 'username'])):
        pid = proc.pid
        name = proc.name()

        #adds process only if the name is not duplicated
        if name not in process_names:
            Lb.insert(idx, name)

        process_names.add(name)

def create_listbox2(name, idx):
    Lb2.insert(idx, name)

def check_status(id):
    lol = psutil.win_service_get(id)
    if lol.STATUS_RUNNING:
        pass

Lb = tk.Listbox(root, selectmode =MULTIPLE)
Lb2 = tk.Listbox(root, selectmode =SINGLE)
Lb.pack()
Lb2.pack()
Lb.place(relx=0.9, rely=0.8, relwidth = 0.5, relheight=0.5, anchor='s')
Lb2.place(relx=0.35, rely=0.8, relwidth = 0.5, relheight=0.5, anchor='s')
Lb.bind('<<ListboxSelect>>', selecta)
create_listbox()

cur_process()
root.update()
root.mainloop()






