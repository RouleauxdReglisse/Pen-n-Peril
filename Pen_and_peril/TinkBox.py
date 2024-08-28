import tkinter as tink
import time
def outline(screen,points,tag):
    for i in range(0,len(points),2):
            screen.create_line([points[i],points[i+1],points[(i+2)%len(points)],points[(i+3)%len(points)]],tags=tag)

class Timer:
    def __init__(self):
        self.FpsTimer=time.time()

    def stall(self,FPS):
        while not time.time()-self.FpsTimer>=1/FPS:
            time.sleep(1/(2**8))
        self.FpsTimer=time.time()
