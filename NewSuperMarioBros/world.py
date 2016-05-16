#levEditor.py

from pygame import *
import os
import pickle

def drawAll(screen, level,guy):
    if base in ('world4','base4'):
        screen.blit(back, (-guy[X],-210-guy[Y]))
    else:screen.blit(back, (-guy[X],-guy[Y]))
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
    myPFile = open(save+".p", "wb")
    pickle.dump(level, myPFile)

def moveScreen(guy):
    keys=key.get_pressed()
    
    if keys[K_LEFT] and guy[X] > 0:
        guy[X] -= 16
    if keys[K_RIGHT] and guy[X] < SCREENX*16:
        guy[X] += 16
    if keys[K_UP] and guy[Y] > 0:
        guy[Y] -= 16
    if keys[K_DOWN] and guy[Y] < SCREENY*16:
        guy[Y] += 16

X=0
Y=1
guy=[0,3]
        
size = width, height = 640,480


col = [(0,0,0),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0),
       (255,0,255),(0,255,255),(125,125,125),(125,250,0),(67,145,42),
       (234,186,90),(31,244,63),(90,87,32),(3,6,9),(77,64,233),(86,32,54)
       ,(90,123,234), (45,33,10),(52,126,255),(33,255,98),(80,46,124),
       (123,234,231)]

current = 1     # my current paint colour / contents
base = input("Enter base: ")
back = image.load(base+".png")
levx,levy=0,0

SCREENX = back.get_width()//16
SCREENY = back.get_height()//16

load = input("Enter loadmap: ")
save = input("Enter savename: ")
level = loadMap(load+".p")         
running = True
myClock = time.Clock()
let = [i for i in "qwertyuiopasdfghjklzxcvbnm"]
screen = display.set_mode(size)
while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False
            
    keys = key.get_pressed()                # get numbers from KB
    #for i in range(len(col)):
     #   if keys[i+48]:
      #      current = i

    for i in range(len(let)):
        if keys[ord(let[i])]:
            current = i
            
    if keys[K_LEFT] and levx > 0:
        levx -= 16
    if keys[K_RIGHT] and levx < SCREENX*16:
        levx += 16
    if keys[K_UP] and levy > 0:
        levy -= 16
    if keys[K_DOWN] and levy < SCREENY*16:
        levy += 16
        
    if mouse.get_pressed()[0]==1:
        mx, my = mouse.get_pos()
        gx = (mx+levx)// 16
        gy = (my+levy)// 16
        level[gx][gy] = current
        #draw.rect(screen, col[level[gx][gy]], (gx*16, gy*16, 15, 15))

    lx,ly=mouse.get_pos()
    #print((lx+guy[X])//16,(ly+guy[Y])//16)
    screen.fill((0,0,0))
    moveScreen(guy)
    drawAll(screen, level,guy)
    display.flip()

    myClock.tick(100)                        
    
quit()

saveMap(level, save+".p")
