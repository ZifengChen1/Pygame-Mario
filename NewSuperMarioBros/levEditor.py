#levEditor.py

from pygame import *
import os
import pickle

def drawAll(screen, level,guy):
    screen.blit(back, (-guy[X],-guy[Y]))
    for x in range(SCREENX):
        for y in range(SCREENY):
            c = level[x][y]
            sqr = Rect(x*16,y*16,15,15).move(-guy[X],-guy[Y])
            if c > 0:
                draw.rect(screen, col[c], sqr)

def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")        # load my board that I pickled
        return pickle.load(myPFile)       
    else:
        return [[0]*SCREENY for x in range(SCREENX)]
    

def saveMap(level, fname):
    myPFile = open("level2.p", "wb")
    pickle.dump(level, myPFile)

def moveScreen(guy):
    keys=key.get_pressed()
    
    if keys[K_LEFT] and guy[X] > 0:
        guy[X] -= 16
    if keys[K_RIGHT] and guy[X] < 2560:
        guy[X] += 16
    if keys[K_UP] and guy[Y]>0:
        guy[Y] -= 16
    if keys[K_DOWN] and guy[Y]<144:
        guy[Y] += 16

X=0
Y=1
guy=[0,144]
        
size = width, height = 640,480
screen = display.set_mode(size)

col = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]

SCREENX = 200
SCREENY = 39

current = 1     # my current paint colour / contents
back = image.load("levpic1.jpg")
levx,levy=0,0
level = loadMap("level2.p")         
running = True
myClock = time.Clock()
let = [i for i in 'qwertyuiopasdfghjklzxcvbnm']
while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False
            
    keys = key.get_pressed()                # get numbers from KB
    for i in range(8):
        if keys[i+48]:
            current = i
        
    if mouse.get_pressed()[0]==1:
        mx, my = mouse.get_pos()
        gx = (mx+guy[X])// 16
        gy = (my+guy[Y])// 16
        level[gx][gy] = current
        #draw.rect(screen, col[level[gx][gy]], (gx*16, gy*16, 15, 15))

    lx,ly=mouse.get_pos()
    #print((lx+guy[X])//16,(ly+guy[Y])//16)

    moveScreen(guy)
    drawAll(screen, level,guy)
    display.flip()

    myClock.tick(100)                        
    
quit()
saveMap(level, "level2.p")
