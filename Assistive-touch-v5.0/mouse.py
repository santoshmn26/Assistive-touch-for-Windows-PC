from pynput.mouse import Listener
import win32api, win32con
import time



def on_click(x,y,button,pressed):
    print("Mouse moved at {0},{1}".format(x,y))
    if((x,y) not in loc):
        loc.append((x,y))
    print(loc)
    if(x==0):
        listener.stop()
        exit
        
def click(x):
    win32api.SetCursorPos((x[0],x[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x[0],x[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x[0],x[1],0,0)
    time.sleep(3)
    for i in loc:
        click(i)
        time.sleep(2)

loc=[]
with Listener(on_click=on_click) as listener:
    listener.join()
    

        
