from Globals import *
import TinkBox

class Enemy:
    def __init__(self,player):
        self.count=0
        self.moveList=[]
        self.pattern=[]
        self.phaseTimer=time.time()
        self.player=player
        self.projectiles=[]
        self.toBurst=[]
        self.pos=[250,100]
        self.shotTotal=0
        self.drawMonster()

    def upkeep(self):
        self.trajectory()
        if self.count>=600 or (self.count>=120 and self.pattern==[self.rest]):
            self.phaseChange()
            self.count=0
        self.count+=1
        for elem in self.pattern:
            if elem!=None:
                elem()

    def shoot(self,start,vectors,shape,tags):
        self.shotTotal+=1
        #[[x,y],[vectorx,vector[y],shape,size,tags]
        self.projectiles.append([start,vectors,shape,"ID:"+str(self.shotTotal),tags])

    def angleVector(self,angle,speed=1):
        vectors=[sin(angle)*speed,cos(angle)*speed]
        return vectors
    
    def vectorAngle(self,vectors):
        if vectors[1]==0:
            angle=90
            if vectors[0]<0:
                angle+=180
        else:
            angle=arctan(vectors[0]/vectors[1])
            if vectors[1]<0:
                angle=(angle+180)%360
        return angle


    def trajectory(self):
        copy=[]
        for elem in self.projectiles:
            copy.append(elem)
        for elem in copy:
            pos,vectors,shape,id,tags=elem
            pos[0]+=vectors[0]
            pos[1]+=vectors[1]
            if (pos[0]<=0-shape[0] or pos[1]<=0-shape[0] or pos[0]>=500+shape[0] or pos[1]>=800+shape[0]) and ("permanent" not in tags and shape[1]!="beam"):
                if "bounce" in tags:
                    if pos[0]>=500 or pos[0]<=0:
                        vectors[0]*=1
                    else:
                        vectors[1]*=-1
                else:
                    game.screen.delete(id)
                    self.projectiles.remove(elem)
            else:
                self.tagHandler(elem)
                if self.count%1==0:
                    if elem in self.projectiles:
                        coords=self.drawShot(pos,shape,id)
                        if "harmless" not in tags:
                            if (coords==-1):
                                if self.circleCollision(shape[0],pos):
                                    self.player.damage()
                            elif self.collision(coords):
                                self.player.damage()

    def drawShot(self,pos,shape,id):
        shapeType=shape[1]
        game.screen.delete(id)
        if shapeType=="polygon":
            size,shapeType,angle,edges=shape
            corners=[]
            startAngle=angle
            for i in range(edges):
                corner=[sin(startAngle+i*(360/edges)),cos(startAngle+i*(360/edges))]
                corners.append(corner)
            coords=[]
            for corner in corners:
                coords.append(pos[0]+size*corner[0])
                coords.append(pos[1]+size*corner[1])
            game.screen.create_polygon(coords,tags=id,fill="white",stipple="gray50",outline="black")
        elif shapeType=="beam":
            size,shapeType,angle=shape
            coords=[]
            for i in range(2):
                coords.append(pos[0]+sin(angle-90+180*i)*(size/2))
                coords.append(pos[1]+cos(angle-90+180*i)*(size/2))
            theta=arctan((size/2)/800)
            coords.append(pos[0]+sin(angle+theta)*math.sqrt(800**2+(size/2)**2))
            coords.append(pos[1]+cos(angle+theta)*math.sqrt(800**2+(size/2)**2))
            coords.append(pos[0]+sin(angle-theta)*math.sqrt(800**2+(size/2)**2))
            coords.append(pos[1]+cos(angle-theta)*math.sqrt(800**2+(size/2)**2))
            game.screen.create_polygon(coords,tags=id,fill="navy blue",stipple="gray50")
        elif shapeType=="circle":
            radius,shapeType=shape
            corners=[pos[0]+radius,pos[1]+radius,pos[0]-radius,pos[1]-radius]
            game.screen.create_oval(corners[0],corners[1],corners[2],corners[3],fill="white",stipple="gray50",tags=id,outline="black")
            return -1
        return coords

    def collision(self,edges):
        if edges==-1:
            pass
        else:
            points=[]
            for i in range(0,len(edges),2):
                coord1=edges[i],edges[i+1]
                coord2=edges[(i+2)%len(edges)],edges[(i+3)%len(edges)]
                if coord1[0]>coord2[0]:
                    coord1,coord2=coord2,coord1
                if coord1[0]<=self.player.pos[0] and coord2[0]>self.player.pos[0]:
                    m=(coord2[1]-coord1[1])/(coord2[0]-coord1[0])
                    c=coord1[1]-m*coord1[0]
                    yCept=self.player.pos[0]*m+c
                    points.append(yCept)
            if len(points)==2:
                if (points[0]>self.player.pos[1])!=(points[1]>self.player.pos[1]):
                    return True
            else:
                return False
            
    def circleCollision(self,size,pos):
        distance=math.sqrt((pos[0]-self.player.pos[0])**2+(pos[1]-self.player.pos[1])**2)
        if distance<size:
            return True
        else:
            return False
        
    def drawMonster(self):
        x=self.pos[0]-80
        y=self.pos[1]+50
        body=[x+0,y+0,x+62,y+-138,x+97,y+-99,x+121,y+-135,x+156,y+0]
        for i in range(0,len(body),2):
            game.screen.create_line([body[i],body[i+1],body[(i+2)%len(body)],body[(i+3)%len(body)]],tags="monster")
        game.screen.create_polygon([x+40,y+-85,x+56,y+-68,x+77,y+-80,x+91,y+-67,x+103,y+-80,x+118,y+-70,x+133,y+-88,x+145,y+-47,x+130,y+-36,x+108,y+-53,x+91,y+-39,x+74,y+-52,x+55,y+-43,x+30,y+-64],fill="black",tags="monster")
        game.screen.create_polygon([x+64,y+-115,x+70,y+-109,x+63,y+-105],fill="black",tags="monster")
        game.screen.create_polygon([x+119,y+-111,x+124,y+-104,x+116,y+-102],fill="black",tags="monster")

    def phaseChange(self):
        self.toBurst=[]
        self.count=0
        if self.pattern==[self.rest]:
            if len(self.moveList)>0:
                self.pattern=self.moveList.pop(0)
                
            else:
                game.screen.delete("monster")
                self.pattern=[None]
        else:
            self.pattern=[self.rest]

    def loadPatterns(self,moveList):
        self.moveList+=moveList
        self.phaseChange()
    
    def loadDemo(self):
        self.loadPatterns([[self.spewPattern],[self.sideWallsPattern],[self.trailPattern]])

    def loadEasy(self):
        pool=[self.ambushPattern,self.mineFieldPattern,self.spinBeamPattern,self.rainPattern,self.stormPattern,self.sideWallsPattern,self.fungusPattern]
        patterns=[[self.spewPattern],[self.dropBlockPattern],[self.beamIntroPattern]]
        for i in range(5):
            choice=random.choice(pool)
            patterns.append([choice])
            pool.remove(choice)

        patterns.append([self.wormPattern])
        patterns.append([self.laserBoxPattern])
        self.loadPatterns(patterns)

    def tagHandler(self,projectile):
        pos,vectors,shape,id,tags=projectile
        if shape[1]=="polygon":
            size,shapeType,angle,edges=shape
        elif shape[1]=="beam":
            size,shapeType,angle=shape
        for i in range(len(tags)):
            if tags[i]=="spin":
                    shape[2]+=tags[i+1]
            elif tags[i]=="turnHoming":
                degree=tags[i+1]
                magnitude=math.sqrt(vectors[0]**2+vectors[1]**2)
                angle=self.vectorAngle(vectors)
                xDiff=self.player.pos[0]-pos[0]
                yDiff=self.player.pos[1]-pos[1]
                targetAngle=self.vectorAngle([xDiff,yDiff])
                if not angle==targetAngle:
                    if (targetAngle-angle)%360>=180:
                        angle-=degree
                        shape[2]-=degree
                    else:
                        angle+=degree
                        shape[2]+=degree
                newVectors=self.angleVector(angle)
                vectors[0]=newVectors[0]*magnitude
                vectors[1]=newVectors[1]*magnitude
            elif tags[i]=="gravHoming":
                maxSpeed=tags[i+2]
                degree=tags[i+1]
                xDiff=self.player.pos[0]-pos[0]
                yDiff=self.player.pos[1]-pos[1]
                adjust=self.angleVector(self.vectorAngle([xDiff,yDiff]))
                newX=vectors[0]+adjust[0]*degree
                newY=vectors[1]+adjust[1]*degree
                if math.sqrt(newX**2+newY**2)<=maxSpeed:
                    vectors[0]=newX
                    vectors[1]=newY
                else:
                    ratio=self.angleVector(self.vectorAngle([newX,newY]))
                    vectors[0]=ratio[0]*maxSpeed
                    vectors[1]=ratio[1]*maxSpeed
            elif tags[i]=="trail":
                count,frequency,extraTags=tags[i+1:i+4]
                if count%frequency==0:
                    tags[i+1]=0
                    self.shoot([pos[0],pos[1]],[0,0],[shape[0],shape[1],shape[2],shape[3]],extraTags)
                tags[i+1]+=1
            elif tags[i]=="sequence":
                count,end=tags[i+1:i+3]
                if count==end:
                    projectile[4]=tags[i+3:len(tags)]
                else:
                    tags[i+1]+=1
                break
            elif tags[i]=="cycle":
                count,end,cycles,endCycles=tags[i+1:i+5]
                if count==end:
                    tags[i+1]=0
                    if cycles!=endCycles:
                        tags[i+3]+=1
                        copy=tags[0:i+5]
                        projectile[4]=tags[i+5:len(tags)]+copy
                    else:
                        projectile[4]=tags[i+5:len(tags)]
                else:
                    tags[i+1]+=1
                break
            elif tags[i]=="worm":
                game.screen.delete(id+"w")
                count,delay,parts,trail=tags[i+1:i+5]
                trail[count]=[pos[0],pos[1]]
                tags[i+1]=(tags[i+1]+1)%len(trail)
                for part in range(len(parts)):
                    copy=(count-delay*(part+1))%len(trail)
                    parts[part][0]=trail[copy][0]
                    parts[part][1]=trail[copy][1]
                    partPos=parts[part]
                    coords=self.drawShot(partPos,shape,id+"w"+str(part))
                    if self.collision(coords):
                        self.player.damage()
            elif tags[i]=="grow":
                newSize=shape[0]+tags[i+1]
                if newSize>=0:
                    shape[0]+=tags[i+1]
            elif tags[i]=="expire":
                if tags[i+1]==tags[i+2]:
                    self.projectiles.remove(projectile)
                    game.screen.delete(id)
                else:
                    tags[i+1]+=1
            elif tags[i]=="burst":
                self.toBurst.append(projectile)
            elif tags[i]=="accelerate":
                increment=tags[i+1]
                if not(vectors[0]==0 and vectors[1]==0):
                    xInc=increment*vectors[0]/math.sqrt(vectors[0]**2+vectors[1]**2)
                    yInc=increment*vectors[1]/math.sqrt(vectors[0]**2+vectors[1]**2)
                    if increment<0 and ((vectors[0]+xInc>0)!=(vectors[0]>=0) and (vectors[1]+yInc>0)!=(vectors[1]>=0)):
                        vectors[0]=0
                        vectors[1]=0
                    else:
                        vectors[0]+=xInc
                        vectors[1]+=yInc
            elif tags[i]=="swerve":
                swerveVectors=tags[i+1]
                vectors[0]+=swerveVectors[0]
                vectors[1]+=swerveVectors[1]





    