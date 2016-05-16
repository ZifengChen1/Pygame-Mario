from pygame import *
from mariotry import *
#from menu import *

class Level:

    def __init__(self,lvl=1):

        self.tilemap = level
        self.colmap = world
        self.tiles = []
        self.coins = []
        
        for x in range(SCREENX):
            for y in range(SCREENY):
                col = self.tilemap[x][y]
                sides = str(self.colmap[x][y])
                rect = Rect(x*16,y*16,16,16)
                tile = ''
                current =0
                
                if col == 1:
                    current = SolidBrick(rect,'')
                if col == 2:
                    current = Question(rect,'')
                if col == 3: pass
                
                if col == 4:
                    current = Brick(rect,'')
                
                if col == 5:
                    current = Question(rect,'')
            
                if col == 6:
                    current = Coin(rect,'')
                '''
                if col == 7:
                    if self.tilemap[x-1][y] != col:
                        tile = 'lefttop'
                    else: tile = 'righttop'

                    if self.tilemap[x][y-1] == col and self.tilemap[x-1][y] != col:
                        tile = 'leftmid'
                    else: tile = 'rightmid'
                    current = Pipe(rect,tile)
                '''
                if col == 10:
                    rect.y += 8
                    current = Flagpole(rect,'flag')
                    
                if current != 0:
                    self.tiles.append(current)
                    
    def refresh(self,cell,col): #PROBLEMS
        for tile in self.tiles:
            if tile.rect == cell:
                ind = self.tiles.index(tile)
                if col == 4:
                    #game.characters.append(BrickBreak(cell,'brickbreak'))
                    del self.tiles[ind]
                elif col == 6:
                    del self.tiles[ind]      
                else:
                    self.tiles[ind] = SolidBrick(cell,'')
    
class SolidBrick:
    def __init__(self,rect,pos):
        self.frame = 0 
        self.image = image.load("pics\\solidbrick.png")
        self.image.set_colorkey((255,255,255))
        self.rect = Rect(rect)
        self.pos = pos
    def update(self): pass
    
class Question:
    def __init__(self,rect,pos):
        self.pics = [image.load("pics\\question%s.png" %str(i+1)) for i in range(4)]
        for i in self.pics: i.set_colorkey((255,255,255))
        self.frame = 0 
        self.image = self.pics[self.frame]
        self.rect = Rect(rect)
        self.pos = pos

    def update(self):
        self.frame += 1
        self.image = self.pics[int(self.frame/4)%4]
                     
class Coin:
    def __init__(self,rect,pos):
        self.pics = [image.load("pics\\coin%s.png" %str(i+1)) for i in range(4)]
        self.frame = 0 
        self.image = self.pics[self.frame]
        self.rect = Rect(rect)
        self.pos = pos

    def update(self):
        self.frame += 1
        self.image = self.pics[int(self.frame/4)%4]
        

class Brick:

    def __init__(self,rect,pos):
        self.pics = [image.load("pics\\brick%s.png" %str(i+1)) for i in range(4)]
        self.frame = 0
        self.image = self.pics[self.frame]
        self.rect = Rect(rect)
        self.pos = pos

    def update(self):
        self.frame += 1
        self.image = self.pics[int(self.frame/4)%4]

class BrickBreak:
    def __init__(self,rect,ch):
        self.img1 = self.img3 = image.load("brickbreak1.png")
        self.img2 = self.img4 = image.load("brickbreak2.png")
        self.rect = Rect(rect)
        self.pos1 = [i for i in rect.topleft]
        self.pos2 = rect.midtop
        self.pos3 = rect.midleft
        self.pos4 = rect.midright

        self.ch = ch
    def update(self):
        self.pos1[0] -= 1
        self.pos1[1] += 2
        topscreen.blit(self.img1,self.pos1)
        
class Flagpole:
    def __init__(self,rect,pos):
        self.pics = [image.load("pics\\flag%s.png" %str(i)) for i in range(32)]
        self.frame = 0
        self.image = self.pics[self.frame]
        self.rect = Rect(rect)
        self.pos = pos

    def update(self):
        self.frame += 1
        self.image = self.pics[int(self.frame/2)%32]
