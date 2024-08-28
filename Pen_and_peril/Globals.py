import tkinter as tink
import time
import random
import math

def cos(theta):
    radians=(theta/360)*2*math.pi
    return round(math.cos(radians),4)
def sin(theta):
    radians=(theta/360)*2*math.pi
    return round(math.sin(radians),4)
def tan(theta):
    radians=(theta/360)*2*math.pi
    return round(math.tan(radians),4)
def arccos(theta):
    radians=math.acos(theta)
    return radians/(2*math.pi)*360
def arcsin(theta):
    radians=math.asin(theta)
    return radians/(2*math.pi)*360,
def arctan(theta):
    radians=math.atan(theta)
    return radians/(2*math.pi)*360

class Game:
    def __init__(self):
        self.testing=False
        self.root=tink.Tk()
        self.root.wm_attributes('-transparentcolor','indigo')
        #99/70 ratio
        self.root.geometry("600x800+100+20")
        self.screen=tink.Canvas()
        self.frameTimer=time.time()
        self.tickSpeed=60

    def makeScreen(self):
        self.screen.destroy()
        self.screen=tink.Canvas(self.root,width=600,height=800)
        self.screen.place(x=0,y=0)
        FPSButton=tink.Button(self.screen,text="enable frame test",command=self.test)
        FPSButton.place(x=0,y=0)
        self.margin=tink.Canvas(self.screen,width=100,height=800,highlightthickness=0)
        self.margin.create_line([0,0,0,800],fill="red")
        self.margin.place(x=500,y=0)
        self.margin.create_oval([50,180,80,210],fill="indigo")
        self.margin.create_oval([50,600,80,630],fill="indigo")
        for i in range(25):
            self.screen.create_line([0,i*30+30,600,i*30+30])
            self.margin.create_line([-10,i*30+30,100,i*30+30])

    def test(self):
        print("start test")
        self.testing=True
        self.testTimer=time.time()
        self.count=0

    def countFrames(self):
        self.count+=1
        if time.time()-self.testTimer>=1:
                print(self.count)
                self.count=0
                self.testTimer=time.time()

    def stall(self):
        while time.time()-self.frameTimer<1/self.tickSpeed:
            time.sleep(1/480)
            pass
        self.frameTimer=time.time()
        self.root.update()
        if self.testing:
            self.countFrames()


game=Game()