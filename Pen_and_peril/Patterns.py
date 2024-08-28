from Enemy import *
from TagMaker import *

class Enemy(Enemy):
    def targetVectors(self,speed=1):
        hypotenuse=math.sqrt((self.player.pos[0]-self.pos[0])**2+(self.player.pos[1]-self.pos[1])**2)
        vectors=[(self.player.pos[0]-self.pos[0])*speed/hypotenuse,(self.player.pos[1]-self.pos[1])*speed/hypotenuse]
        return vectors

    def rest(self):
        pass

    def fungusPattern(self):
        if self.count%300==1:
            self.fungus()

    def fungus(self):
        for i in range(30):
            start=[self.pos[0],self.pos[1]]
            angle=random.randint(-30,30)
            vectors=self.angleVector(angle)
            speed=random.randint(4,9)
            vectors[0]*=speed
            vectors[1]*=speed
            shape=[6,"polygon",0,4]
            tags=["harmless"]
            sequence(tags,20)
            accelerate(tags,-0.1)
            if random.randint(1,4)==1:
                sequence(tags,random.randint(60,180))
                gravHoming(tags,0.1)
                sequence(tags,2)
                accelerate(tags,0.1)
            else:
                sequence(tags,220)
                grow(tags,-0.1)
                expire(tags,220)
            self.shoot(start,vectors,shape,tags)

    def stormPattern(self):
        if self.count==1:
            self.stormSetup()
        copy=[]
        for elem in self.toBurst:
            copy.append(elem)
        for elem in copy:
            pos,vectors,shape,id,tags=elem
            size,shapeType,angle,sides=shape
            newAngle=angle
            for i in range(sides):
                start=[pos[0],pos[1]]
                vectors=self.angleVector(newAngle)
                multiplier=tags[1]
                vectors[0]*=multiplier
                vectors[1]*=multiplier
                shape=[7,"polygon",newAngle,3]
                newTags=[]
                #accelerate(tags,0.01)
                self.shoot(start,vectors,shape,newTags)
                newAngle+=360/sides
            self.toBurst.remove(elem)

    def stormSetup(self):
        spinRate=0.75
        for i in range(2):
            spinRate*=-1
            start=[self.pos[0],self.pos[1]]
            vectors=[0,6]
            shape=[18,"polygon",0,4]
            tags=[]
            spin(tags,spinRate)
            accelerate(tags,-0.05)
            sequence(tags,120)
            burst(tags)
            spin(tags,spinRate)
            expire(tags,53)
            cycle(tags,0,60)
            spin(tags,spinRate)
            cycle(tags,8,60)
            self.shoot(start,vectors,shape,tags)

    #def stormSetup(self):
     #   spinRate=1
      #  for i in range(3):
       #     start=[self.pos[0],self.pos[1]]
        #    vectors=[0,6]
         #   shape=[18,"polygon",0,4]
          #  tags=[]
           # spin(tags,spinRate)
            #accelerate(tags,-0.05)
            #sequence(tags,120)
            #burst(tags)
            #spin(tags,spinRate)
            #expire(tags,53)
            #cycle(tags,0,60)
            #spin(tags,spinRate)
            #cycle(tags,5,60)
            #self.shoot(start,vectors,shape,tags)
            #spinRate+=1

    def spinBeamPattern(self):
        if self.count==1:
            self.spinBeamSetup()
            if self.count%40==0:
                self.spinBeam()

    def spinBeam(self):
        pass
        
    def spinBeamSetup(self):
        for i in range(4):
            shape=beam(3,i*90)
            tags=[]
            warningBeam(tags,3,30,40)
            spin(tags,1)
            expire(tags,550)
            vectors=[0,0]
            start=[250,500]
            self.shoot(start,vectors,shape,tags)

    def rainPattern(self):
        if self.count%60==1:
            self.rain()

    def rain(self):
        start=[self.pos[0],self.pos[1]]
        vectors=self.targetVectors(4)
        tags=[]
        extraTags=[]
        swerve(extraTags,[0,0.05])
        trail(tags,20,extraTags)
        shape=[10,"polygon",0,5]
        self.shoot(start,vectors,shape,tags)

    def dropBlockPattern(self):
        if self.count%120==60:
            self.dropBlock((self.count//120)%2)

    def dropBlock(self,offset):
        baseStart=offset*50
        for i in range(8):
            vectors=[0,4]
            shape=[50,"polygon",45,4]
            tags=[]
            sequence(tags,50)
            accelerate(tags,-0.1)
            sequence(tags,30)
            start=[baseStart+90*i,0]
            self.shoot(start,vectors,shape,tags)

    def beamIntroPattern(self):
        if self.count==1:
            self.beamIntroSetup()
        elif self.count%20==0 and self.count>=90:
            self.beamIntro(((self.count-90)%300))

    def beamIntro(self,count):
        shape=beam(4,angle=90)
        vectors=[0,0]
        pos=[0,175+40+count*2]
        tags=[]
        warningBeam(tags,4,20,90)
        expire(tags,60)
        self.shoot(pos,vectors,shape,tags)


    def beamIntroSetup(self):
        angle=0
        tags=[]
        warningBeam(tags,2,50,90)
        expire(tags,510)
        self.shoot([50,0],[0,0],beam(2,angle),tags)
        tags=[]
        warningBeam(tags,2,50,90)
        expire(tags,510)
        self.shoot([450,0],[0,0],beam(2,angle),tags)
        angle=90
        tags=[]
        warningBeam(tags,2,50,90)
        expire(tags,510)
        self.shoot([0,500],[0,0],beam(2,angle),tags)
        tags=[]
        warningBeam(tags,2,50,90)
        expire(tags,510)
        self.shoot([0,175],[0,0],beam(2,angle),tags)


    def trailShot(self):
        start=[self.pos[0],self.pos[1]]
        if self.player.pos[1]==self.pos[1]:
            vectors=[1,0]
        else:
            angle=arctan((self.pos[0]-self.player.pos[0])/(self.pos[1]-self.player.pos[1]))
            vectors=self.angleVector(angle)
        speed=6
        vectors[0]*=speed
        vectors[1]*=speed
        tags=[]
        extraTags=[]
        spin(extraTags)
        gravHoming(extraTags,degree=0.05,maxSpeed=5)
        trail(tags,frequency=20,extraTags=extraTags)
        self.shoot(start,vectors,[12,"polygon",0,6],tags)

    def trailPattern(self):
        if self.count%120==0:
            self.trailShot()

    def laserBoxPattern(self):
        if self.count%90==0:
            self.laserBox()
        copy=[]
        for elem in self.toBurst:
            copy.append(elem)
        for elem in copy:
            pos,vectors,shape,id,tags=elem
            angle=shape[2]-45
            for i in range(4):
                start=[pos[0],pos[1]]
                newShape=beam(3,angle)
                newTags=[]
                warningBeam(newTags,3,15,50)
                grow(newTags,0.5)
                sequence(newTags,90)
                expire(newTags)
                self.shoot(start,[0,0],newShape,newTags)
                angle+=90
            self.toBurst.remove(elem)
    
    def laserBox(self):
        start=[self.pos[0],self.pos[1]]
        angle=random.randint(-30,30)
        vectors=self.angleVector(angle)
        speed=random.uniform(5.0,12.0)
        vectors=[vectors[0]*speed,vectors[1]*speed]
        spinAngle=random.randint(0,90)
        shape=[10,"polygon",spinAngle,4]
        tags=[]
        spin(tags,1)
        accelerate(tags,-0.125)
        sequence(tags,120)
        burst(tags)
        sequence(tags,0)
        sequence(tags,60)
        expire(tags)
        self.shoot(start,vectors,shape,tags)

    def spiralPattern(self):
        if self.count%1==0:
            self.spiral(self.count%360)
            

    def spiral(self,count):
        angle=count*5
        vectors=self.angleVector(angle)
        distance=120
        start=[self.player.pos[0]+vectors[0]*distance,self.player.pos[1]+vectors[1]*distance]
        vectors[0]*=-0.125
        vectors[1]*=-0.125
        shape=[4,"polygon",angle+180,3]
        tags=[]
        sequence(tags,60)
        accelerate(tags,0.15)
        expire(tags,45)
        self.shoot(start,vectors,shape,tags)
    
    def mineFieldPattern(self):
        if self.count%200<30 and self.count%200>0:
            self.mineField()

    def ambushPattern(self):
        if self.count%300==1:
            self.ambush()

    def ambush(self):
        for i in range(120):
            angle=i*3
            vectors=self.angleVector(angle)
            distance=90
            start=[self.player.pos[0]+vectors[0]*distance,self.player.pos[1]+vectors[1]*distance]
            vectors[0]*=-0.125
            vectors[1]*=-0.125
            shape=[4,"polygon",angle+180,3]
            tags=[]
            if i%2==0:
                sequence(tags,30+i*2)
                accelerate(tags,0.15)
                expire(tags,45)
            else:
                expire(tags,285)
            self.shoot(start,vectors,shape,tags)
        
    def mineField(self):
        x=random.randint(20,480)
        y=random.randint(220,780)
        start=[x,y]
        vectors=[0,0]
        tags=["harmless"]
        size=random.randint(50,100)
        sequence(tags)
        grow(tags,size/100)
        sequence(tags,60)
        grow(tags,-0.5)
        expire(tags,90)
        self.shoot(start,vectors,[4,"polygon",0,6],tags)

    def wormPattern(self):
        if self.count%600==1:
            self.worm()
        copy=[]
        for elem in self.toBurst:
            copy.append(elem)
        for elem in copy:
            pos,vectors,shape,id,tags=elem
            angle=45
            for i in range(len(tags)):
                if tags[i]=="worm":
                    index=i+3
                    break
            partPos=random.choice(tags[index])
            for i in range(4):
                newVectors=self.angleVector(angle)
                speed=3
                newVectors=[newVectors[0]*speed,newVectors[1]*speed]
                newPos=[partPos[0],partPos[1]]
                newShape=[6,"polygon",angle,3]
                newTags=[]
                self.shoot(newPos,newVectors,newShape,newTags)
                angle+=90
            self.toBurst.remove(elem)
        

    def worm(self):
        start=[self.pos[0],self.pos[1]]
        vectors=[0,1.5]
        tags=["permanent"]
        turnHoming(tags,1)
        worm(tags,start,10,10)
        cycle(tags,30,45)
        burst(tags)
        cycle(tags,0,17)
        self.shoot(start,vectors,[10,"polygon",45,12,],tags)
        
    def redirect(self):
        start=[self.pos[0],self.pos[1]]
        if self.player.pos[1]==self.pos[1]:
            vectors=[1,0]
        else:
            angle=arctan((self.pos[0]-self.player.pos[0])/(self.pos[1]-self.player.pos[1]))
            vectors=self.angleVector(angle)
        speed=4
        vectors[0]*=speed
        vectors[1]*=speed
        tags=["permanent"]
        cycle(tags,60,3)
        gravHoming(tags,99,speed)
        cycle(tags,3,3)
        self.shoot(start,vectors,[12,"polygon",0,6],tags)


    def wave(self,start):
        angle=90-start
        while angle>-90:
            vectors=self.angleVector(angle)
            tags=[]
            spin(tags)
            self.shoot(vectors,[20,"polygon",0,4],20,tags)
            angle-=15

    def spewPattern(self):
        if self.count%5==0:
            self.spew()

    def spew(self):
            vectors=self.angleVector(random.randint(-90,90))
            speed=random.randint(1,6)
            vectors[0]*=speed
            vectors[1]*=speed
            size=random.randint(4,12)
            shape=[size,"polygon",0,random.randint(3,6)]
            tags=[]
            spin(tags)
            self.shoot([self.pos[0],self.pos[1]],vectors,shape,tags)


    def sideWallsPattern(self):
        if self.count%60==0:
            self.sideWalls(self.count%120//60)

    def sideWalls(self,step):
        for i in range(16):
                startY=self.pos[1]+i*80+40
                if step==0:
                    vectors=[-1,0]
                    startY+=40
                    startX=500
                else:
                    vectors=[1,0]
                    startX=0
                speed=3
                vectors[0]*=speed
                vectors[1]*=speed
                self.shoot([startX,startY],vectors,[24,"polygon",0,5],[])

    def wavePattern(self):
        if self.count%30==0:
            self.wave((self.count%(30*4)//30)*(15/4))

    #remilia scralet lookin ass
    def redMagicPattern(self):
        if self.count%180==1:
            self.redMagic()
        if self.count%180==60:
            self.pos=[random.randint(100,400),random.randint(50,150)]
            game.screen.delete("monster")
            self.drawMonster()
        copy=[]
        for elem in self.toBurst:
            copy.append(elem)
        for elem in copy:
            pos,vectors,shape,id,tags=elem
            start=[pos[0],pos[1]]
            newVectors=self.angleVector((self.count%180)+180+self.vectorAngle(vectors),0.1)
            #newVectors=self.angleVector(arctan(pos[0]/pos[1]),0.1)
            newTags=[]
            sequence(newTags,180-(self.count)%180)
            swerve(newTags,newVectors)
            sequence(newTags,5)
            newShape=circle(9)
            self.shoot(start,[0,0],newShape,newTags)
            self.toBurst.remove(elem)

    def redMagic(self):
        angle=0
        for i in range(10):
            start=[self.pos[0],self.pos[1]]
            vectors=self.angleVector(angle,2)
            shape=circle(30)
            tags=["bounce"]
            cycle(tags,20,16)
            burst(tags)
            cycle(tags,0,16)
            self.shoot(start,vectors,shape,tags)
            angle+=36

    def testPattern(self):
        if self.count%120==0:
            self.test()

    def test(self):
        direction=1
        for i in range(2):
            direction*=-1
            angle=0
            for i in range(36):
                start=[self.pos[0],self.pos[1]]
                vectors=self.angleVector(angle,2)
                vectors[0]+=0.5*direction
                shape=polygon(3,angle,3)
                tags=[]
                self.shoot(start,vectors,shape,tags)
                angle+=10

    def moonSignPattern(self):
        if self.count%30<10 and self.count%2==1:
            self.moonSign(self.count%60//30)
        if self.count%120==0:
            self.pos=[random.randint(100,400),random.randint(50,150)]
            game.screen.delete("monster")
            self.drawMonster()
        if self.count%3==0:
            self.moonDrops()

    def moonSign(self,beat):
        angle=self.vectorAngle(self.targetVectors())+beat*7.5
        for i in range(24):
            start=[self.pos[0],self.pos[1]]
            vectors=self.angleVector(angle,4)
            shape=circle(4)
            tags=[]
            self.shoot(start,vectors,shape,tags)
            angle+=15

    def moonDrops(self):
        for i in range(1):
            start=[random.randint(0,500),random.randint(50,150)]
            vectors=[0,random.randint(2,4)]
            shape=circle(4)
            tags=[]
            self.shoot(start,vectors,shape,tags)
        


