#levEditor.py

from pygame import *
import os
import pickle
from pprint import *

def drawAll(screen, level,guy):
    screen.blit(back, (-guy[X],-guy[Y]))
    for x in range(SCREENX):
        for y in range(SCREENY):
            c = str(level[x][y])
            sqr = Rect(x*16,y*16,16,16).move(-guy[X],-guy[Y])
            if 'w' in c or 'a' in c or 's' in c or 'd' in c:
                draw.rect(screen,(255,0,0),sqr,2)      
                
def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")        # load my board that I pickled
        return pickle.load(myPFile)       
    else:
        return [[0]*SCREENY for x in range(SCREENX)]
    

def saveMap(level, fname):
    myPFile = open(fname, "wb")
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
screen = display.set_mode(size)

let = ['w','a','d','s']

current = ''     # my current paint colour / contents
pic = input("enter background image: ")
back = image.load(pic+".png")
levx,levy=0,0

SCREENX = back.get_width()//16
SCREENY = back.get_height()//16
base = input("Enter loadmap: ")
save = input("Enter savefilename: ")
level = loadMap(base+".p")

running = True
myClock = time.Clock()
while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False
            
    keys = key.get_pressed()                # get numbers from KB
    
    current = ''
    if keys[K_w]:
        current += 'w'
    if keys[K_a]:
        current += 'a'
    if keys[K_s]:
        current += 's'
    if keys[K_d]:
        current += 'd'
    if keys[K_q]:
        current = "was"
    if keys[K_e]:
        current = 'wsd'
    if keys[K_SPACE]:
        current = 'wasd'
    
            
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
        print(current)
        #draw.rect(screen, col[level[gx][gy]], (gx*16, gy*16, 15, 15))

    lx,ly=mouse.get_pos()
    #print((lx+guy[X])//16,(ly+guy[Y])//16)

    screen.fill((0,0,0))
    moveScreen(guy)
    drawAll(screen, level,guy)
    display.flip()

    myClock.tick(100)                        
    
quit()
saveMap(level,save+".p")
