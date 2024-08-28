def gravHoming(list,degree=0.1,maxSpeed=5):
    tag=["gravHoming",degree,maxSpeed]
    list+=tag

def turnHoming(list,degree=1):
    tag=["turnHoming",degree]
    list+=tag

def spin(list,degree=1):
    tag=["spin",degree]
    list+=tag

def trail(list,frequency=30,extraTags=[]):
    tag=["trail",0,frequency,extraTags]
    list+=tag

def sequence(list,delay=30):
    tag=["sequence",0,delay]
    list+=tag

def cycle(list,delay=30,maxCycles=3):
    tag=["cycle",0,delay,0,maxCycles]
    list+=tag

def worm(list,start,parts=5,delay=15):
    #ist 1 holds the stats for the segments
    #list 2 holds the past moves
    tag=["worm",0,delay,[],[]]
    for i in range(delay*(parts+1)):
        tag[4].append([start[0],start[1]])
    for i in range(parts):
        tag[3].append([start[0],start[1]])
    list+=tag

def beam(width=5,angle=0):
    shape=[width,"beam",angle]
    return shape
def polygon(size,angle,sides):
    shape=[size,"polygon",angle,sides]
    return shape
def circle(radius):
    shape=[radius,"circle"]
    return shape

def grow(list,increment=1):
    tag=["grow",increment]
    list+=tag

def warningBeam(list,startSize,maxSize,duration=30):
    tags=["harmless"]
    sequence(tags,duration)
    grow(tags,(maxSize-startSize)/10)
    sequence(tags,10)
    list+=tags

def burst(list):
    tags=["burst"]
    list+=tags

def expire(list,countdown=60):
    tags=[]
    tags+=["expire",0,countdown]
    list+=tags

def accelerate(list,increment):
    tags=["accelerate",increment]
    list+=tags

def swerve(list,vectors):
    tags=["swerve",vectors]
    list+=tags

def bounce(list):
    tags=["bounce"]
    list+=tags
