from Globals import *
class Player:
    def __init__(self):
        self.pos=[270,450]
        self.focusMode=False
        self.vectors=[0,0]
        self.angle=0
        self.lives=5
        self.iFrames=0
        self.activeDirections=[]
        game.root.bind("<a>",self.go)
        game.root.bind("<d>",self.go)
        game.root.bind("<w>",self.go)
        game.root.bind("<s>",self.go)
        game.root.bind("<A>",self.go)
        game.root.bind("<D>",self.go)
        game.root.bind("<W>",self.go)
        game.root.bind("<S>",self.go)
        game.root.bind("<Shift_L>",self.focus)
        game.root.bind("<KeyRelease>",self.stop)
        self.draw()
        x=50
        y=290
        for i in range(self.lives):
            game.margin.create_polygon([x+0,y+0,x+-16,y+-17,x+-28,y+2,x+-5,y+29,x+20,y+4,x+8,y+-12],fill="pink",tags="heart"+str(i))
            y+=60
        
    def focus(self,inp):
        if inp.keysym=="Shift_L":
            self.focusMode=True

    def go(self,inp):
        inp.keysym=inp.keysym.lower()
        shorthand={"a":[-1,0],"d":[1,0],"w":[0,-1],"s":[0,1]}
        if inp.keysym in "wasd" and not inp.keysym in self.activeDirections:
            direction=shorthand[inp.keysym]
            self.vectors[0]+=direction[0]
            self.vectors[1]+=direction[1]
            self.activeDirections.append(inp.keysym)
        if inp.keysym=="shift_l":
            self.focusMode=True

    def stop(self,inp):
        inp.keysym=inp.keysym.lower()
        shorthand={"a":[-1,0],"d":[1,0],"w":[0,-1],"s":[0,1]}
        if inp.keysym in self.activeDirections:
            direction=shorthand[inp.keysym]
            self.vectors[0]-=direction[0]
            self.vectors[1]-=direction[1]
            self.activeDirections.remove(inp.keysym)
        if inp.keysym=="shift_l":
            self.focusMode=False
    
    def damage(self):
        if self.iFrames<=0:
            self.lives-=1
            game.margin.delete("heart"+str(self.lives))
            self.iFrames=60
        
    def move(self):
        if self.iFrames>0:
            self.iFrames-=1
        speed=2
        if self.focusMode==True:
            speed=1
        yDest=self.pos[1]+self.vectors[1]*speed
        xDest=self.pos[0]+self.vectors[0]*speed
        if xDest>0 and xDest<500:
            self.pos[0]=xDest
            if abs(self.angle)<=20:
                self.angle-=self.vectors[0]*2
        if  yDest<800 and yDest>200:
            self.pos[1]=yDest
        #angle means cape angle
        if self.angle!=0:
            diff=self.angle/abs(self.angle)
            self.angle-=diff
        self.draw()

    def draw(self):
        game.screen.delete("player")
        if self.iFrames%4==0 or self.iFrames<=10:
            radius=5
            capeLen=15
            arc=30
            capeAngle=self.angle
            lCapeX=sin(self.angle+capeAngle+arc)
            lCapeY=cos(self.angle+capeAngle+arc)
            rCapeX=sin(self.angle+capeAngle-arc)
            rCapeY=cos(self.angle+capeAngle-arc)
            game.screen.create_polygon([self.pos[0],self.pos[1],self.pos[0]+capeLen*rCapeX,self.pos[1]+capeLen*rCapeY,self.pos[0]+capeLen*lCapeX,self.pos[1]+capeLen*lCapeY],outline="black",fill="blue",width=3,tags="player")
            game.screen.create_oval([self.pos[0]+radius,self.pos[1]+radius,self.pos[0]-radius,self.pos[1]-radius],outline="black",fill="white",width=3,tags="player")
            if self.focusMode==True:
                game.screen.create_oval([self.pos[0]+1,self.pos[1]+1,self.pos[0]-1,self.pos[1]-1],fill="red",width=1,tags="player")