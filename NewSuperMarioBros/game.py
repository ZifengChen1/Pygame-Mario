from pygame import *
import os
import pickle
from random import *
from math import *


class Level:

    def __init__(self,lvl=1):
        self.tilemap = game.tilemap             #all tiles and blocks
        self.colmap = game.colmap               #collision
        self.lvlnum = lvl
        self.tiles = []
        self.coins = []
        count = 0
        for x in range(game.SCREENX):
            for y in range(game.SCREENY):
                col = self.tilemap[x][y]
                sides = str(self.colmap[x][y])
                rect = Rect(x*16,y*16,16,16)
                tile = ''
                current =0

                #bricks
                
                if col == 1:
                    current = SolidBrick(rect,'solbrick')
                    self.colmap[x][y] = 'wasd'
                    
                if col == 2:
                    current = Question(rect,'powerupblock')
                    self.colmap[x][y] = 'wasd'
                    
                if col == 3:
                    current = Question(rect,'lifeblock')
                    self.colmap[x][y] = 'wasd'
                    
                if col == 4:
                    current = Brick(rect,'brick')
                    if lvl == 2:
                        current = BlueBrick(rect,'bluebrick')
                    self.colmap[x][y] = 'wasd'
                    
                if col == 5:
                    current = Question(rect,'question')
                    self.colmap[x][y] = 'wasd'
                    
            
                if col == 6:
                    current = Coin(rect,'coin')
                
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
                    
                if col == 11:
                    current = StarCoin(rect,'starcoin',count)
                    count += 1
                    
                if current != 0:
                    self.tiles.append(current)
                    
    def refresh(self,cell,col):             #updates all tiles when collided with
        for tile in self.tiles:
            if tile.rect == cell:
                ind = self.tiles.index(tile)
                if col == 4:
                    #game.characters.append(BrickBreak(cell,'brickbreak'))
                    del self.tiles[ind]
                elif col == 6:
                    del self.tiles[ind]
                elif col == 11: pass
                    
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
        self.up = -1

    def update(self):
        self.frame += 1
        self.image = self.pics[int(self.frame/4)%4]
        
class StarCoin:
    def __init__(self,rect,pos,count):
        self.pics = [image.load("pics\\starcoin%s.png" %str(i)) for i in range(32)]
        self.frame = 0
        self.hit = False
        self.image = self.pics[self.frame]
        self.rect = Rect((rect[0],rect[1]),self.image.get_size())
        self.pos = pos
        self.count = count

    def update(self):
        self.rect.x += (self.rect.width-self.image.get_width())
        self.rect.width = self.image.get_width()
        self.frame += 1
        self.image = self.pics[self.frame%32]
        
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

class BlueBrick(Brick):

    def __init__(self,rect,pos):
        self.pics = [image.load("pics\\bluebrick%s.png" %str(i)) for i in range(4)]
        self.frame = 0
        self.image = self.pics[self.frame]
        self.rect = Rect(rect)
        self.pos = pos
    
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
        
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target)

def complex_camera(camera, target):
    l, t, _, _ = target
    _, _, w, h = camera
    l, t, _, _ = -l+HALFWIDTH, -t+HALFHEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-game.SCREENX*16), l)         # stop scrolling at the right edge
    t = max(-(camera.height-game.SCREENY*16), t)        # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top

    if game.lvl.lvlnum == 2:
        return Rect(l, t-128, w, h)
    elif game.lvl.lvlnum ==3:
        return Rect(l, -144, w, h)
    elif game.lvl.lvlnum ==4:
        return Rect(l, -80, w, h)
    elif game.lvl.lvlnum == 5:
        return Rect(l, t-90, w, h)
    
    return Rect(l, -112, w, h)
                
class Mario:
    norm = 0
    sup = 1
    fire = 2
    def __init__(self,x,y,colour,ch):
        
        self.rightpics = [[],[],[]]
        self.rightpics[norm].append([image.load("normalmove//normalidle%s.png" %str(i)) for i in range(17)])
        self.rightpics[norm].append([image.load("normalmove//normalhop%s.png" %str(i)) for i in range(5)])
        self.rightpics[norm].append([image.load("normalmove//normalrun%s.png" %str(i)) for i in range(12)])
        self.rightpics[norm].append([image.load("normalmove//normalwalk%s.png" %str(i)) for i in range(10)])
        self.rightpics[norm].append([image.load("normalmove//normalduck.png")])
        self.rightpics[norm].append([image.load("normalmove//normalpound%s.png" %str(i)) for i in range(13)])
        
        self.rightpics[sup].append([image.load("supermove//superstand%s.png" %str(i)) for i in range(45)])
        self.rightpics[sup].append([image.load("supermove//superjump%s.png" %str(i+1)) for i in range(18)])
        self.rightpics[sup].append([image.load("supermove//superwalk%s.png" %str(i)) for i in range(25)])
        self.rightpics[sup].append([image.load("supermove//superrun%s.png" %str(i)) for i in range(18)])
        self.rightpics[sup].append([image.load("supermove//superduck.png")])
        self.rightpics[sup].append([image.load("supermove//superpound%s.png" %str(i)) for i in range(13)])

        self.rightpics[fire].append([image.load("firemove//firestand%s.png" %str(i)) for i in range(24)])
        self.rightpics[fire].append([image.load("firemove//firejump%s.png" %str(i)) for i in range(33)])
        self.rightpics[fire].append([image.load("firemove//firewalk%s.png" %str(i)) for i in range(22)])
        self.rightpics[fire].append([image.load("firemove//firerun%s.png" %str(i)) for i in range(18)])
        self.rightpics[fire].append([image.load("firemove//fireduck.png")])
        self.rightpics[fire].append([image.load("firemove//firepound%s.png" %str(i)) for i in range(13)])
        self.rightpics[fire].append([image.load("firemove//firethrow%s.png" %str(i)) for i in range(6)])
        
        self.leftpics = [[[0]*17,[0]*5,[0]*12,[0]*10,[0],[0]*13],
                         [[0]*45,[0]*18,[0]*25,[0]*18,[0],[0]*13],
                         [[0]*24,[0]*33,[0]*22,[0]*18,[0],[0]*13,[0]*6]]
        
        for i in range(len(self.rightpics)):
            for j in range(len(self.rightpics[i])):
                for k in range(len(self.rightpics[i][j])):
                    self.leftpics[i][j][k] = transform.flip(self.rightpics[i][j][k],True,False)
                
        self.action = 0 #what mario is doing ex walking running
        self.type = norm #how big mario is
        self.pics = self.rightpics[self.type][self.action]
        self.frame = 0
        self.image = self.pics[self.frame]

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.last = self.rect.copy()

        self.resting = False #if mario is on ground
        self.kapowie = False #ground pound
        self.ch = ch  #characters
        self.colour = colour
        self.lastact = 0
        
        self.peak = 0 #counter used in various ways
        self.dy = 0
        self.hp = 1
        self.lives = 3
        self.direction = 1

        self.invincible = 0

    def move(self):
        
        keys = key.get_pressed()
        self.peak += 1
        
        if keys[K_x]:
            speed = 5
        else:
            speed = 3
            
        if keys[K_z] and self.resting: #jump
            self.dy = -13
            
        if keys[K_LEFT]:
            self.rect.x -= speed
            self.direction = -1
            self.action = 2
            if speed == 5: self.action = 3 
            
        elif keys[K_RIGHT]:
            self.rect.x += speed
            self.direction = 1
            self.action = 2
            if speed == 5: self.action = 3
        elif keys[K_DOWN]:
            if self.dy>4 or self.dy<-4:
                if self.lastact != 5:
                    self.frame = 0
                self.kapowie = True
                self.action = 5
                self.dy += 1
            else:
                if self.lastact != 5: #what mario does in previous loop
                    self.action = 4
            if self.lastact == 5:
                self.frame = -3
                if self.hp == 1: self.frame = -1
        else: self.action = 0

        if keys[K_DOWN] and (keys[K_LEFT] or keys[K_RIGHT]):
            self.action = 4
                
        if keys[K_c] and self.type == fire and self.peak >= 20:
            if len([ch.ch for ch in game.characters if ch.ch == 'fireball'])<2:
                self.action = 6
                pics = [image.load("pics//fireball%s.png" %str(i)) for i in range(4)]
                fireball = Fireball(self.rect.midtop[0]+(8*self.direction),self.rect.centery,(250,250,0),'fireball',pics)
                fireball.newrect()
                fireball.direction = self.direction
                game.characters.append(fireball)
            self.peak = 0
            
        self.lastact = self.action
        
        if self.dy<0:
            if self.lastact != 1: self.frame = 0
            self.action = 1
            
        if self.resting == False:
            self.rect.y += self.dy
            self.dy += 1
        self.resting = False

    def collide(self):

        self.last = self.rect.copy()

        self.move()

        self.rect.y += (self.rect.height-self.image.get_height())
        self.rect.height = self.image.get_height()

        x1 = self.rect.x//16
        y1 = self.rect.y//16

        x2 = x1+3
        p = y1+4
        if self.hp == 1:
            p = y1+3
            

        for x in range(x1-1,x2):
            for y in range(y1-1,p):
                hi = str(game.colmap[x][y])
                c = game.tilemap[x][y]
                cell = Rect(x*16,y*16,16,16)

                if self.rect.colliderect(cell):
                    if c == 21:
                        self.hp = 0
                    if c == 6 or c==11:
                        game.tilemap[x][y] = 0
                        game.lvl.refresh(cell,c)
                        game.pts += 100
                        game.coincount += 1
                        
                    if 'a' in hi and self.last.right <= cell.left and self.rect.right > cell.left:  #right collision
                        self.rect.right = cell.left
                        self.action = 0 
                        
                    if 'd' in hi and self.last.left >= cell.right and self.rect.left < cell.right:  #left collision
                        self.rect.left = cell.right
                        self.action = 0
                        
                    if 'w' in hi and self.last.bottom <= cell.top and self.rect.bottom > cell.top:  #top collision 
                        self.resting = True
                        self.rect.bottom = cell.top
                        self.dy = 0
                        if self.kapowie:
                            if c==2:
                                if self.hp == 1:
                                    ch = 'mushroom'
                                    pics = [image.load("pics//mushroom%s.png" %str(i)) for i in range(7)]
                                elif self.hp>=2:
                                    ch = 'fireflower'
                                    pics = [image.load("pics//fireflower%s.png" %str(i)) for i in range(3)]
                                powerup = PowerUp(x*16,y*16,(255,0,0),ch,pics)
                                game.characters.append(powerup)
                                game.characters[-1].up = 1
                                game.tilemap[x][y] = 1
                                game.pts += 1000
                            if c==3:
                                pics = [image.load("pics//life%s.png" %str(i)) for i in range(7)]
                                life = Life(x*16,y*16,(255,0,0),'life',pics)
                                game.characters.append(life)
                                game.characters[-1].up = 1
                                game.tilemap[x][y] = 1
                                game.pts += 1000
                            if c==4:  #breaks bricks and makes it passable
                                game.tilemap[x][y] = 0
                                game.colmap[x][y] = '0'

                            if c==5:  #coin brick
                                game.lvl.tiles.append(Coin((x*16,(y+1)*16,16,16),'temp'))
                                game.lvl.tiles[-1].up = 1
                                game.tilemap[x][y] = 1
                                game.colmap[x][y] = 'wasd'
                                game.pts += 100
                                game.coincount += 1
                        

                            game.lvl.refresh(cell,c)
                        self.kapowie=False
    
                    if 's' in hi and self.last.top >= cell.bottom and self.rect.top < cell.bottom:  #bottom collision
                        self.rect.top = cell.bottom
                        self.dy = 0
        
                        if c==2:
                            if self.hp == 1:
                                ch = 'mushroom'
                                pics = [image.load("pics//mushroom%s.png" %str(i)) for i in range(7)]
                            elif self.hp>=2:
                                ch = 'fireflower'
                                pics = [image.load("pics//fireflower%s.png" %str(i)) for i in range(3)]
                            powerup = PowerUp(x*16,y*16,(255,0,0),ch,pics)
                            game.characters.append(powerup)
                            game.characters[-1].up = -1
                            game.tilemap[x][y] = 1
                            game.pts += 1000

                        if c==3:   #one up
                            pics = [image.load("pics//life%s.png" %str(i)) for i in range(7)]
                            life = Life(x*16,y*16,(255,0,0),'life',pics)
                            game.characters.append(life)
                            game.characters[-1].up = -1
                            game.tilemap[x][y] = 1
                            game.pts += 1000
                            
                        if c==4:  #breaks bricks
                            game.tilemap[x][y] = 0
                            game.colmap[x][y] = '0'
                            
                        if c==5:   #coins
                            game.lvl.tiles.append(Coin((x*16,(y-1)*16,16,16),'temp'))
                            game.tilemap[x][y] = 1
                            game.colmap[x][y] = 'wasd'
                            game.pts += 100
                            game.coincount += 1
                            
                        game.lvl.refresh(cell,c)
        
    def update(self):
        
        self.type = self.hp - 1
        self.invincible += 1
        
        if self.hp <= 0:
            del game.characters[game.characters.index(game.player)]
            
        for ch in game.characters:
            ind = game.characters.index(ch)
            
            if game.SCREENY>self.rect.y//16<0:
                del game.characters[ind]
                
            if self.rect.colliderect(ch.rect) and ch != self:
                
                if ch.ch == 'goomba':
                    if self.last.bottom <= ch.rect.top and self.rect.bottom>=ch.rect.top:
                        self.rect.bottom = ch.rect.top
                        self.dy = -10
                        img = image.load("pics//goombasmush.png")
                        game.characters[ind] = Death([img],ch.rect,'dead',ind)
                        game.pts += 200
                        
                    else:
                        if self.invincible>= 50:   #if mario gets killed, his hp goes down one, and he's temporarily invincible
                            self.hp-=1
                            self.invincible = 0
                    
                
                elif ch.ch in ('mushroom','fireflower'):
                    last = self.hp
                    
                    del game.characters[ind]
                    
                    if ch.ch == 'mushroom':
                        self.hp = 2
                    if ch.ch == 'fireflower':
                        self.hp = 3
                    if last != self.hp:
                        self.levelup(last)
                    else:
                        game.item.ch = 'fireitem'

                elif ch.ch == 'life':
                    self.lives += 1
                    del game.characters[ind]
                    
                elif ch.ch=='jumpkoopa':
                    if self.last.bottom<= ch.rect.top and self.rect.bottom >= ch.rect.top:
                        self.dy = -12
                        self.rect.y += self.dy

                        #turns jumping koopa to regular koopas
                        game.characters[ind] = Koopa(ch.rect.x,ch.rect.y,(0,0,0),'koopa',[image.load("pics//koopawalk%s.png" %str(i)) for i in range(16)])
                        game.characters[ind].direction = ch.direction
                        
                    else:
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0
                        
                elif ch.ch=='koopa':
                    if self.last.bottom<= ch.rect.top and self.rect.bottom>=ch.rect.top:
                        self.dy = -12
                        self.rect.y += self.dy
                        #turns koopas to koopashell
                        game.characters[ind] = Koopashell(ch.rect.x,ch.rect.y,(0,122,0),'koopashell',[image.load("pics//koopashell%s.png" %str(i)) for i in range(3)])
                        game.pts += 200
                    else:
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0
                        
                elif ch.ch=='koopashell':
                    #direction of shells based on where he got kicked
                    if self.last.centerx<=ch.rect.centerx and ch.kick==False:
                        ch.direction=1
                    elif self.last.centerx>=ch.rect.centerx and ch.kick==False:
                        ch.direction=-1
                    if self.last.bottom <= ch.rect.top and self.rect.bottom>=ch.rect.top:
                        self.dy = -16
                        ch.kick=False
                        ch.num+=1
                    #kicking shells from the sides 
                    elif self.last.right<=ch.rect.left and self.rect.right>=ch.rect.left and ch.kick==False:
                        ch.direction=1
                        ch.kick=True
                        ch.num=1
                    elif self.last.left>=ch.rect.right and self.rect.left<=ch.rect.right and ch.kick==False:
                        ch.direction=-1
                        ch.kick=True
                        ch.num=1
                    elif self.rect.colliderect(Rect(ch.rect.centerx-6,ch.rect.centery-6,12,12)) and ch.kick==True:
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0

                    #number of times mario jumps on shell and corresponding movement
                    if ch.num%2==1:
                        ch.kick=True
                        
                elif ch.ch == 'piranhaplant':
                    if int(ch.frame/3)%len(ch.pics) in range(6,17):
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0
                        
                elif ch.ch=='lakitu':
                    if self.last.bottom <= ch.rect.top and self.rect.bottom>=ch.rect.top:
                        self.rect.bottom = ch.rect.top
                        self.dy = -10
                        del game.characters[ind]
                        
                elif ch.ch == 'spiny':
                    if self.rect.colliderect(ch.rect):
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0
                        
                elif ch.ch == 'bulletbill':
                    #Can't pass through bulletbill
                    if self.last.left >= ch.rect.right and self.rect.left < ch.rect.right:
                        self.rect.left = ch.rect.right
                        
                    if self.last.right <= ch.rect.left and self.rect.right > ch.rect.left:
                        self.rect.right = ch.rect.left
                        
                    if self.last.bottom >= ch.rect.top and self.rect.bottom > ch.rect.top:
                        self.rect.bottom = ch.rect.top
                        
                elif ch.ch == 'bill':
                    
                    if self.last.bottom <= ch.rect.top and self.rect.bottom > ch.rect.top:
                        del game.characters[ind]
                        self.dy = -12
                        game.pts += 100
                    else:
                        if self.invincible>= 50:
                            self.hp-=1
                            self.invincible = 0

                elif ch.ch == 'bowser':
                    if ch.bowsershell == False:
                        if self.last.bottom <= Rect(ch.rect).top and self.rect.bottom > Rect(ch.rect).top:
                            ch.bowserhit += 1                    
                            ch.bowsershell = True
                            ch.rect = (ch.rect[0], ch.rect[1]+32, 48,32)
                            self.dy = -12
                        
                        else:
                            self.hp -= 1
                    else:
                        self.hp -= 1

                elif ch.ch == 'smallfire' or ch.ch == 'boo' or ch.ch == 'thwomp' or ch.ch == 'lavabubble':
                    self.hp -= 1

                
                    
        self.collide()
        self.draw()
        
        if self.direction == 1:
            self.pics = self.rightpics[self.type][self.action]
        elif self.direction == -1:
            self.pics = self.leftpics[self.type][self.action]

        self.frame += 1
        #Changes rate of picture blitting
        #Based on numbe of images
        if self.action == 2:
            dv = 2.3
            if self.hp>= 2: dv = 0.9
        elif self.action == 3:
            dv = 1.5
            if self.hp >=2: dv = 0.9
        elif self.action == 5: dv = 1.7
        else: dv = 4
        
        self.image = self.pics[int(self.frame/dv)%len(self.pics)]
        
    def levelup(self,last):
        
        pics = [self.rightpics[last-1][self.action][0],self.rightpics[self.hp-1][self.action][0]]
        self.peak = 0
        x1 = self.rect.x//16
        y1 = self.rect.y//16

        x2 = x1+3
        p = y1+4
        if self.hp == 1:
            p = y1+3

        #Pauses game and blits picture of previous ad new mario
        while True:            
            self.peak += 1
            
            image = pics[int(self.peak/8)%len(pics)]

            self.rect.y += (self.rect.height-self.image.get_height())
            self.rect.height = self.image.get_height()
            
            topscreen.blit(game.scene,(0,-127))
            topscreen.blit(game.base,game.cam.apply(game.base.get_rect()))

            for ch in game.characters:
                if ch.ch != 'mario':
                    topscreen.blit(ch.image,game.cam.apply(Rect(ch.rect)))
                        
            for tile in game.lvl.tiles:
                rect = game.cam.apply(tile.rect)
                topscreen.blit(tile.image,rect)
                
            topscreen.blit(image,game.cam.apply(self.rect))

            if self.peak == 42: return
            screen.blit(topscreen,(0,0))
            
            display.flip()
                               
    def finish(self,tile):
        
        self.frame = 0
        self.dy = 2
        touch = False #Checks whether mario is on ground or not
        fall = image.load("normalmove//normalfall.png")
        clear = image.load("pics//marioclear.png")
        paste = [480,75]
        if self.type == norm:
            done = [image.load("normalmove//normalfinish%s.png" %str(i)) for i in range(35)]
        elif self.type == sup:
            done = [image.load("supermove//superfinish%s.png" %str(i)) for i in range(35)]
        else:
            done = [image.load("firemove//firefinish%s.png" %str(i)) for i in range(35)]

        mixer.music.load("mario music//lvlfinish.mid")
        mixer.music.play(1)
        
        g = tile.rect.y #Position of flag
        
        while True:
            game.clock.tick(30)
            self.frame += 1
            
            if self.resting == False:
                self.rect.y += self.dy
                if touch:
                    self.dy += 0.25
            
            if not touch:
                
                self.rect.x = tile.rect.x+tile.rect.width #Mario falls
                self.pics = [fall]                          #Flag falls
                
            elif touch:
                if paste[0] >= (480-clear.get_width())/2: #"mario clear' comes across screen
                    paste[0] -= 4
                if self.pics != done:
                    self.pics = self.rightpics[self.type][2]
                    self.rect.x += 2

            if tile.rect.y < g+7*16:
                tile.rect.y += 2

            
            self.resting = False
    
            self.rect.y += (self.rect.height-self.image.get_height())
            self.rect.height = self.image.get_height()

            x1 = self.rect.x//16
            y1 = self.rect.y//16

            x2 = x1+3
            p = y1+4
            if self.hp == 1:
                p = y1+3
                
            for x in range(x1-1,x2): #Checks collision
                for y in range(y1-1,p):
                    hi = str(game.colmap[x][y])
                    c = game.tilemap[x][y]
                    cell = Rect(x*16,y*16,16,16)
                    if self.rect.colliderect(cell):
                        if 'w' in hi and self.last.bottom <= cell.top and self.rect.bottom > cell.top:
                            self.resting = True
                            self.rect.bottom = cell.top
                            self.dy = 0
                            touch = True
                            
            if self.rect.x >= self.last.x+5*16:
                if self.pics != done:
                    self.frame = 0
                self.pics = done
                if int(self.frame/1.5) == len(self.pics)-1:
                    
                    game.main(game.item.ch,game.pts,game.coincount,self.lives,self.hp,game.lvl.lvlnum+1)
                
            self.image = self.pics[int(self.frame/1.5)%len(self.pics)]
            tile.update()
            
            topscreen.blit(game.scene,(0,-127))
            topscreen.blit(tile.image,game.cam.apply(tile.rect))
            topscreen.blit(game.base,game.cam.apply(game.base.get_rect()))
            topscreen.blit(clear,paste)
            self.draw()
            screen.blit(topscreen,(0,0))
            display.flip()
            
    def die(self):

        self.peak = 0
        self.type = 0
        self.action = 4
        self.frame = 0
        
        self.rightpics[self.type].append([image.load("normalmove//normaldie%s.png" %str(i)) for i in range(9)])
        self.pics = self.rightpics[self.type][-1]
        self.dy = -6

        dying = True
        #Pauses game, mario dies
        #transitions into deathscreen function
        while dying:
            game.clock.tick(30)
            self.peak += 1
            
            self.image = self.pics[int(self.frame/3)%len(self.pics)]
            
            if int(self.frame/3) in range(3,6):
                
                self.rect.y -= 2
            elif int(self.frame/3)>=6:
                self.rect.y += int(self.dy)
                
            self.dy += 0.2
            topscreen.blit(game.scene,(0,-127))
            topscreen.blit(game.base,game.cam.apply(game.base.get_rect()))

            for tile in game.lvl.tiles:
                rect = game.cam.apply(tile.rect)
                topscreen.blit(tile.image,rect)
                
            for ch in game.characters:
                ch.draw()
                
            if int(self.frame/3) == len(self.pics)-1:
                self.pics = [image.load("normalmove//normaldie%s.png" %str(i+6)) for i in range(3)]

            if self.peak <= 100:
                self.draw()
            else: dying = False
            
            screen.blit(topscreen,(0,0))
            self.frame += 1
            
            display.flip()
        if self.lives>0:
            deathscreen()
        else:
            deathscreen(True)
        return
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(self.rect))       
                    
class Enemy:
    
    def __init__(self,x,y,colour,ch,pics,speed=-1,direction=1,up=-1):
        
        self.leftpics = pics
        self.rightpics = [transform.flip(self.leftpics[i],True,False) for i in range(len(pics))]
        self.frame = 0
        self.image = self.leftpics[self.frame]
        
        self.rect = Rect((x,y),(16,16))
        self.last = self.rect.copy()

        self.resting = False
        self.ch = ch
        self.colour = colour
        
        self.peak = 0 #Counter for random things
        self.dy = 0
        self.hp = 1
        self.direction = direction
        self.up = up #
        self.speed = speed

        #KOOPA STUFF
        

        self.kick = False
        self.dx=0
        self.num=0 #counter for koopashell

        #LAKITU STUFF
        self.horz=-4 #horizonatal counter for lakitu
        self.hvar=0
        self.interval=0

        self.vert=-1  #counter for lakitu
        self.var=0

        #SPINY STUFF
        self.hit = False
        
    def move(self):
                    
        if self.resting == False:
            self.rect.y += self.dy
            self.dy += 1
   
        self.resting = False
        
        self.rect.x += self.speed*self.direction

    def collide(self):
        
        self.last = self.rect.copy()
        self.move()
        self.rect.y += (self.rect.height-self.image.get_height())
        self.rect.height = self.image.get_height()
        

        x1 = self.rect.x//16
        y1 = self.rect.y//16

        for x in range(x1-1,x1+3):
            for y in range(y1-1,y1+4):
                hi = str(game.colmap[x][y])
                c = game.tilemap[x][y]
                cell = Rect(x*16,y*16,16,16)
               
                if self.rect.colliderect(cell):
                        
                    if 'a' in hi and self.last.right <= cell.left and self.rect.right > cell.left:
                        self.rect.right = cell.left
                        if self.ch == 'fireball':
                            ind = game.characters.index(self)
                            pics = [image.load("pics//firekill%s.png" %str(i)) for i in range(5)]
                            game.characters[ind] = Death(pics,self.rect,'dead',ind)

                        else: self.direction *= -1
                        
                    if 'd' in hi and self.last.left >= cell.right and self.rect.left < cell.right:
                        self.rect.left = cell.right
                        if self.ch == 'fireball':
                            ind = game.characters.index(self)
                            pics = [image.load("pics//firekill%s.png" %str(i)) for i in range(5)]
                            game.characters[ind] = Death(pics,self.rect,'dead',ind)

                        else: self.direction *= -1
                        
                    if 'w' in hi and self.last.bottom <= cell.top and self.rect.bottom > cell.top:
                        self.resting = True
                        self.rect.bottom = cell.top
                        self.dy = 0
                        self.hit = True

                        self.down = True
    
                    if 's' in hi and self.last.top >= cell.bottom and self.rect.top < cell.bottom:
                        self.rect.top = cell.bottom
                        self.dy = 0

                        if abs(game.player.rect.x - (self.rect.x + (self.rect[2])/2)) <= 60:
                            self.down = False
                        else:
                            self.still = True

    def update(self):
        
        self.frame += 1

        for ch in game.characters:  #enemies change direction after hitting each other
            if ch.ch != 'mario':
                if self.rect.colliderect(ch.rect):
                    if self.ch != 'koopshell' and ch.ch not in ('koopashell','spiny'):
                        self.direction *= -1
                        ch.direction *= -1
        dv = 3
        if self.ch == 'lakitu': dv = 6
        if self.direction == 1:
            self.image = self.leftpics[int(self.frame/dv)%len(self.leftpics)]
        elif self.direction == -1:
            self.image = self.rightpics[int(self.frame/dv)%len(self.rightpics)]
            
        self.collide()
        self.draw()
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(Rect(self.rect)))

class Fireball(Enemy):        
    def newrect(self):
        self.rect.height = 10
        self.rect.width = 10
        self.dy = -6
        
    def move(self):
        
        self.rect.x += 6*self.direction

        if self.resting == False:
            self.rect.y += self.dy
            self.dy += 1
        
        else:
           self.dy = -6

        self.resting = False
            
    def update(self):
        
        for ch in game.characters:
            ind = game.characters.index(ch)
            if self.rect.colliderect(ch.rect):
                if ch.ch not in ('fireball','mario'):
                    if ch.ch == 'goomba':  #kills enemies after hitting them
                        game.characters[ind] = Death([image.load("pics//goombasmush.png")],ch.rect.move(0,16),'dead',ind)
                    else:
                        game.characters[ind] = Death([image.load("pics//koopasmush.png")],ch.rect.move(0,16),'dead',ind)
                    self.leftpics = [image.load("pics//firekill%s.png" %str(i)) for i in range(5)]
                    self.update = self.die  #deletes fireball after collision
                    
                
        self.frame += 1
        self.image = self.leftpics[int(self.frame/2)%len(self.leftpics)]
        self.collide()
        self.draw()
        
    def die(self):
        self.frame += 1
        self.image = self.leftpics[int(self.frame/2)%len(self.leftpics)]
        self.draw()
        if int(self.frame/2)%len(self.leftpics) == 4:
            del game.characters[game.characters.index(self)]
            
class PowerUp(Enemy): #not actually enemy, just similiar class style
    
    def move(self):
        if self.peak<=8:
            self.rect.y += 2*self.up
            self.peak += 1
            
        elif self.ch == 'mushroom' or self.ch == 'life':
            self.rect.x += 1*self.direction

        if self.resting == False and self.peak>8:
            self.rect.y += self.dy
            self.dy += 2
                
        self.resting = False

    def update(self):
        
        self.frame += 1
        if self.direction == 1:
            self.image = self.leftpics[int(self.frame/8)%len(self.leftpics)]
        elif self.direction == -1:
            self.image = self.rightpics[int(self.frame/8)%len(self.rightpics)]
            
        self.collide()
        self.draw()

class Life(PowerUp): pass
        
class Goomba(Enemy): pass

class JumpKoopa(Enemy):
    def move(self):
        if self.resting==False:
            self.rect.y += self.dy
            self.dy += 1
        else:
            self.dy-=randint(4,8)
        
        self.resting = False

        self.rect.x += -1*self.direction
        
class Koopa(Enemy): pass

class Koopashell(Enemy):
        
    def move(self):
        if self.resting == False:
            self.rect.y += self.dy
            self.dy += 1
        
        self.resting = False

        if self.kick == False:   #tells if mario kicked him or not
            self.dx=0
        else:
            self.dx+=8
           
            self.rect.x+=self.dx*self.direction
        self.dx=0

    def update(self):
        if self.kick:
            self.frame += 1

        if not self.kick:
            self.peak += 1

        if self.peak >= 300:
            self.leftpics = [image.load("pics//koopaup%s.png" %str(i)) for i in range(5)]
            self.rightpics = [transform.flip(i,True,False) for i in self.leftpics]
            self.frame += 1
            
        if len(self.leftpics) == 5 and int(self.frame/3)%5 == 4:
            game.characters[game.characters.index(self)] = Koopa(self.rect.x,self.rect.y,(0,0,0),'koopa',[image.load("pics//koopawalk%s.png" %str(i)) for i in range(16)])
                    
        if self.direction == 1:
            self.image = self.leftpics[int(self.frame/3)%len(self.leftpics)]
        elif self.direction == -1:
            self.image = self.rightpics[int(self.frame/3)%len(self.rightpics)]
            
        for ch in game.characters:
            ind = game.characters.index(ch)
            if self.rect.colliderect(ch.rect):
                if ch.ch not in ('koopashell','mario'):  #if it hits other enemies, it kills them
                    if self.kick:
                        if ch.ch == 'goomba':
                            game.characters[ind] = Death([image.load("pics//goombasmush.png")],ch.rect.move(0,16),'dead',ind)
                        else:
                            game.characters[ind] = Death([image.load("pics//koopasmush.png")],ch.rect.move(0,16),'dead',ind)
    
        self.collide()
        self.draw()

class PiranhaPlant:
    
    def __init__(self,x,y,pics,ch='piranhaplant'):
        self.pics = pics
        self.image = pics[0]
        self.frame = 0
        self.ch = ch
        self.direction = 1
        self.rect = Rect((x,y),self.image.get_size())
        self.peak = 0

    def update(self):

        self.rect.y += (self.rect.height-self.image.get_height())
        self.rect.height = self.image.get_height()
        if self.peak%100 in range(0,67):
            self.frame += 1
            self.image = self.pics[int(self.frame/3)%len(self.pics)]
        self.peak += 1
        self.draw()
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(self.rect))
        
class BulletBill:
    
    def __init__(self, x,y,colour,ch,image):
        self.colour = colour
        self.rect = Rect(x,y,16,32)
        self.image = image
        self.ch = ch
        self.counter = 0
        
    def update(self):
        self.draw()
        self.counter += 1

        if self.counter%100 == 1:
            yo = Bill(self.rect.x,self.rect.y,'bill')
            game.characters.append(yo)
            
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(self.rect))

class Bill:
    
    def __init__(self,x,y,ch):
        
        self.rect = Rect(x,y,16,16)
        self.leftpics = [image.load("pics//bulletbill%s.png" %str(i)) for i in range(16)]
        self.rightpics = [transform.flip(i,True,False) for i in self.leftpics]
        
        self.ch = ch
        
        if game.player.rect.x <= self.rect.x:  #changes the direction of shooting depending on mario's position
            self.direction = -1
            self.pics = self.leftpics
        else:
            self.direction = 1
            self.pics = self.rightpics

        self.frame = 0
        self.image = self.pics[self.frame]

    def update(self):

        self.rect.x += 2*self.direction

        self.frame += 1
        self.image = self.pics[int(self.frame/3)%len(self.pics)]
        
        self.draw()
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(self.rect))

class Boo(Enemy):
    def __init__(self,x,y,pics,ch='boo'):
        self.leftpics = pics
        self.rightpics = [transform.flip(i,True,False) for i in self.leftpics]
        self.frame = 0
        
        self.rect = (x,y,16,16)
        self.ch = ch

        self.rightback = [image.load("pics//booturn.png")]
        self.leftback = [transform.flip(self.rightback[0],True,False)]

        self.pics = self.rightback
        self.image = self.pics[0]
        
    def follow(self, r1, r2):
        cx,cy = r2[0] - r1[0], r1[1] - r2[1]                
        ang = atan2(cy, cx) #finds the angle using the slope

        r2 = (r2[0] - 1.5*cos(ang),r2[1] + 1.5*sin(ang), 16, 16)
        return r2
    
    def move(self):
        if abs(game.player.rect.x - self.rect[0]) < 320:
            if game.player.direction == 1:
                self.pics = self.rightback
                if game.player.rect.x > self.rect[0]: #if facing away from boo
                    self.rect = self.follow(game.player.rect, self.rect)
                    self.pics = self.rightpics
            elif game.player.direction == -1:
                self.pics = self.leftback
                if game.player.rect.x < self.rect[0]:
                    self.rect = self.follow(game.player.rect, self.rect)
                    self.pics = self.leftpics


    def update(self):

        self.move()
        self.frame += 1
        self.image = self.pics[int(self.frame/3)%len(self.pics)]
        self.draw()
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(Rect(self.rect)))

class Thwomp(Enemy):
    def __init__(self,x,y,pics,ch):

        self.down = True
        self.dy = 0
        self.frame = 0

        self.pics = pics
        self.image = self.pics[0]

        if ch == 'thwimp': #small thwomp
            self.rect = Rect(x,y,32,37)
        else:
            self.rect = Rect(x,y,64,74)
        self.ch = ch
        self.wait = 0

        self.still = True

        self.direction = 0

        
    def move(self):

        if self.down == False: #thwomp touches top
            self.still = False
            self.image = self.pics[0]
            self.wait = 0
            self.rect.y += self.dy
            self.dy += 0.3
        elif self.down == True: #thwomp touches bottom
            if self.wait >= 25:
                self.image = self.pics[1]
                self.dy = 0
                self.rect.y -= 1
            self.wait += 1

        if self.still == True:
            self.image = self.pics[2]
    
            
    def update(self):
        self.collide()
        
        self.frame += 1
        
        topscreen.blit(self.image,game.cam.apply(self.rect))


class Lavabubble(Enemy):
    def __init__(self,x,y,pics,ch):
        self.pics = pics
        self.image = self.pics[3]
        self.rect = (x,y,16,16)
        self.ch = ch
        self.dy = 5
        self.x, self.y = x,y
        self.wait = 0
    def move(self):

        if self.wait == 0:
            self.dy -= 0.14
            self.rect = (self.rect[0], self.rect[1] - self.dy, 16, 16)
        if self.dy <= -5:
            self.wait += 1
        if self.wait > 28:
            self.wait = 0
            self.rect = (self.x,self.y,16,16)
            self.dy = 5

    def update(self):
        self.move()
        topscreen.blit(self.image,game.cam.apply(Rect(self.rect)))
       
class Lakitu(Enemy):

    def move(self):

        #moves him up and down
        self.interval+=1
        stuff = game.player
        
        self.var+=self.vert
        self.rect.y+=self.vert
        if self.var==24 or self.var==-16:
            self.vert*=-1
        
       #moves him left and right and follows maro around
        self.hvar+=self.horz
        self.rect.x+=self.horz
        if stuff.direction==1:
            if self.rect.x>(stuff.rect.x-300) and self.rect.x<(stuff.rect.x-randint(100,275)):
                self.horz=7
            elif self.rect.x>(stuff.rect.x+randint(100,275)) and self.rect.x<(stuff.rect.x+300):
                self.horz=-5
        elif stuff.direction==-1:
            if self.rect.x>(stuff.rect.x-300) and self.rect.x<(stuff.rect.x-randint(100,275)):
                self.horz=5
            elif self.rect.x>(stuff.rect.x+randint(100,275)) and self.rect.x<(stuff.rect.x+300):
                self.horz=-7        
        #direction of enemy based on position of  mario
        if self.interval%randint(65,85)==0:
            enemy=Spiny(self.rect.x,self.rect.y,(255,255,255),'spiny',[image.load("pics//spinyfall%s.png" %str(i)) for i in range(4)])
            if enemy.resting==True:
                if enemy.rect.centerx>stuff.rect.centerx:
                    enemy.direction=-1
                elif enemy.rect.centerx<=stuff.rect.centerx:
                    enemy.direction=1
            
            game.characters.append(enemy)
    
class Spiny(Enemy):
    def move(self):
        
        self.rect.x+=1*self.direction
        
        if self.resting == False:
            self.rect.y += (self.dy//4)
            self.dy += 2
        if self.hit:
            self.rightpics = [image.load("pics//spinywalk%s.png" %str(i)) for i in range(4)]
            self.leftpics = [transform.flip(i,True,False) for i in self.rightpics]
            self.hit = False
            
        self.resting = False

    


#BOSS BOWSER ###################################################   

class Bowser:
    def __init__(self,x,y,pics,ch):
        
        self.startdy = 15 #set dy, doesnt change
        self.dy = 15

        self.ty = 12 #bowser shell jumps

        self.leftpics = pics
        self.rightpics = [transform.flip(i,True,False) for i in self.leftpics]
        self.image = self.rightpics[0]
        self.speed = 1
        #if bowser turns into shell form
        self.shell = 0

        self.ch = ch

        self.bowserhit = 0 #number of times bowser is hit
        self.bowsershell = False #checks if bowser is in shell form 
          
        self.rect = (x,y, self.image.get_size()[0],self.image.get_size()[1])
        self.last = Rect(self.rect).copy()

        self.direction = 1

        self.resting = True

        
        self.frequency = 30 #the counter which controls what actions bowser takes at a certain time

        self.spitfrequency = 0 #the rate at which bowser spits fire

        self.x = self.rect[0]
        self.y = self.rect[1]
        self.ychange = 0.6
        
        self.above = False

        self.defined = False
        
    def bowserjump(self):

        if abs(int(self.rect[0]) - game.player.rect.x) < 4:
            self.above = True
            self.dy = 1
            

        if self.above == True:          
            self.rect = (self.rect[0], self.rect[1]+18,  self.image.get_size()[0],self.image.get_size()[1])
            self.dy = 1
    
        else:
            self.dy += -0.6
            xchange = (self.rect[0] - game.player.rect.x)/15
            self.rect = (self.rect[0] - xchange, self.rect[1] - self.dy, self.image.get_size()[0],self.image.get_size()[1])

    def bcollide(self):
        
        
        self.last = Rect(self.rect).copy()
        self.travel()
        self.Brect = Rect(self.rect)
        self.Brect.y += (self.Brect.height-self.image.get_height())
        self.Brect.height = self.image.get_height()
        

        x1 = self.Brect[0]//16
        y1 = self.Brect[1]//16

        for x in range(x1-1,x1+6):
            for y in range(y1-1,y1+5):
                hi = str(game.colmap[x][y])
                c = game.tilemap[x][y]
                cell = Rect(x*16,y*16,16,16)
               
                if self.Brect.colliderect(cell):

                        
                    if 'a' in hi and self.last.right <= cell.left and self.Brect.right > cell.left:
                        self.Brect.right = cell.left
                        self.direction *= -1
                        
                        
                    if 'd' in hi and self.last.left >= cell.right and self.Brect.left < cell.right:
                        self.Brect.left = cell.right
                        self.direction *= -1
                        
                        
                    if 'w' in hi and self.last.bottom <= cell.top and self.Brect.bottom > cell.top:
                        self.Brect.bottom = cell.top
                        self.ty = 12
                        self.rect = (self.rect[0], self.y, 32, 48)
                        if self.above == True:
                            self.above = False
                            self.frequency += 1
                            self.dy = 15

    
                    if 's' in hi and self.last.top >= cell.bottom and self.Brect.top < cell.bottom:
                        self.Brect.top = cell.bottom
                        


        
    def travel(self):
        if self.bowserhit == 3:
            print('YOU WON')
            quit()
        if self.direction == 1:
            if self.bowsershell == True:
                self.image = self.rightpics[21]
            else:
                self.image = self.leftpics[0]
            if self.above == True:
                self.image = self.rightpics[18]
                
        else:
            if self.bowsershell == True:
                self.image = self.leftpics[21]
            else:
                self.image = self.rightpics[0]
            if self.above == True:
                self.image = self.leftpics[18]
        
        if self.bowsershell == False:
            self.rect = (self.rect[0],self.rect[1], self.image.get_size()[0],self.image.get_size()[1])
            if self.frequency == 50:

                if self.spitfrequency %50 == 25:
                    bowserfireA = Smallfire(self.rect[0], self.rect[1] + 7, 'smallfire')
                    game.characters.append(bowserfireA)
        
                if self.spitfrequency == (self.bowserhit)*50 + 50:
                    self.frequency = 0
                    self.spitfrequency = 0
 

                self.spitfrequency += 1

            if self.bowserhit >= 1:
                if self.frequency == 20:
                    self.bowserjump()

                if self.frequency != 50 and self.frequency != 20:
                    self.frequency += 1

            else:
                if self.frequency != 50:
                    self.frequency += 1

            if self.frequency != 50 and self.frequency != 20:
                if game.player.rect.x >= self.rect[0]:
                    self.direction = 1
                else:
                    self.direction = -1


                if self.bowserhit == 0:
                    self.speed = 0.5
                elif self.bowserhit == 1:
                    self.speed = 0.75
                elif self.bowserhit == 2:
                    self.speed = 1

                self.rect = (self.rect[0] + self.speed * self.direction, self.rect[1],  self.image.get_size()[0],self.image.get_size()[1])

        elif self.bowsershell == True:
            #if self.defined == False:
            self.rect = (self.rect[0], self.y + self.image.get_size()[1]/2, self.image.get_size()[0],self.image.get_size()[1])                
            self.defined = True

            self.shell += 1
            if 50<self.shell<300:
                if self.bowserhit == 1:
                    self.rect = (self.rect[0] + 10*self.direction, self.rect[1],  self.image.get_size()[0],self.image.get_size()[1])
                elif self.bowserhit == 2:
                    self.ty += -1.5
                    self.rect = (self.rect[0] + 7*self.direction, self.rect[1] - self.ty,  self.image.get_size()[0],self.image.get_size()[1])

                    
            elif self.shell >= 300:
                self.bowsershell = False
                self.defined = False
                self.rect = (self.rect[0], self.y,  self.image.get_size()[0],self.image.get_size()[1])
                self.shell = 0
                self.frequency = 40

        
       
    def update(self):
 
        self.bcollide()
        self.draw()
        
    def draw(self):
        topscreen.blit(self.image,game.cam.apply(Rect(self.rect)))

        
class Smallfire(Bowser):
    def __init__(self,x,y,ch='smallfire'):
        self.pics = [transform.scale(image.load("pics//fireball%s.png" %str(i)),(24,24)) for i in range(4)]
        self.frame = 0
        self.image = self.pics[0]
        self.rect = Rect(x,randint(int(y) + 5, int(y)+20),24,24)
        self.ch = ch
        if game.player.rect.x <= self.rect.x:
            self.direction = -1
        else:
            self.direction = 1

    def update(self):
        self.frame += 1
        self.image = self.pics[self.frame%len(self.pics)]
        self.rect.x += 3*self.direction
        topscreen.blit(self.image,game.cam.apply(self.rect))

#################################################
       
class Death:
    def __init__(self,pics,rect,ch,ind):
        self.pics = pics
        self.frame = 0
        self.image = self.pics[0]
        self.rect = rect
        self.ch = ch
        self.peak = 0
        self.ind = ind
        self.direction = 1

    def update(self):
        
        self.rect.y += (self.rect.height-self.image.get_height())
        self.rect.height = self.image.get_height()
        
        self.peak += 1
        self.frame +=1
        self.image = self.pics[int(self.frame/3)%len(self.pics)]
        
        if self.peak <12:
            self.draw()
            
        elif self.ind<len(game.characters):
            del game.characters[self.ind]

    def draw(self):
        topscreen.blit(self.image,game.cam.apply(self.rect))

        
class Item:
    def __init__(self,ch='noitem'):
        self.ch = ch
        self.pics = [Surface((56,56))]
        self.frame = 0
        self.image = self.pics[0]
        self.image.set_alpha(0)
        self.rect = Rect((365,220),self.image.get_size())
        self.peak = 0
        
    def update(self):

        if self.ch == 'fireitem':
            self.pics = [image.load("pics//fireitem%s.png" %str(i)) for i in range(3)]

        else:
            self.pics = [Surface((56,56))]
        self.peak += 1
        self.rect.y += (self.rect.height-self.image.get_height())
        self.rect.height = self.image.get_height()

        if self.peak >= 50:
            self.frame += 1
            self.image = self.pics[int(self.frame/4)%len(self.pics)]
            
        if int(self.frame/4)%len(self.pics) == len(self.pics)-1:
            self.peak = 0
            
        self.draw()

    def draw(self):
        btmscreen.blit(self.image,self.rect)
        
class Game:
    
    def main(self,item='noitem',score=0,coins=0,lives=3,hp=1,lvl=1):
        self.clock = time.Clock()
        self.characters = []
        self.pts = score
        self.base = image.load("base%s.png" %str(lvl))
        self.tilemap = loadMap("level%s.p" %str(lvl))
        self.colmap = loadMap("collide%s.p" %str(lvl))
        self.SCREENX = self.base.get_width()//16
        self.SCREENY = self.base.get_height()//16
        print(self.SCREENX,self.SCREENY)

        arrow = image.load("arrow.png")
        self.lvl = Level(lvl)
        
        self.scene = image.load("pics//scene%s.png" %str(lvl))
        loadscreen(lives)
        
        self.item = Item()
        self.item.ch = item
        self.starcount = [0]*3
        starpos = [(73,252),(134,243),(196,235)]
        btmstar = image.load("pics//btmstar.png")

        self.coincount = coins
        
        ptsimg = [image.load("pics//lives%s.png" %str(i)) for i in range(10)]
        numimg = [image.load("pics//num%s.png" %str(i)) for i in range(8)]
        coinicon = image.load("pics//coin1.png")

        mixer.music.play(-1)
        for x in range(self.SCREENX):
            for y in range(self.SCREENY):
                c = self.tilemap[x][y]
                cell = (x*32,y*32,32,32)
                if c == 8:
                    self.player = Mario(x*16,y*16,(255,255,255),'mario')
                    self.player.hp = hp
                    self.player.lives = lives
                    self.characters.append(self.player)
        
                if c == 9:
                    pics = [image.load("pics//goomba%s.png"%str(i)) for i in range(9)]
                    goomba = Goomba(x*16,y*16,(0,0,0),'goomba',pics)
                    self.characters.append(goomba)
                    
                if c == 12:
                    enemy = Koopa(x*16,y*16,(0,0,0),'koopa',[image.load("pics//koopawalk%s.png" %str(i)) for i in range(16)])
                    self.characters.append(enemy)

                if c == 13:
                    enemy = PiranhaPlant(x*16,(y-2)*16,[image.load("pics//piranhaplant%s.png" %str(i)) for i in range(22)])
                    self.characters.append(enemy)

                if c == 14:
                    enemy = JumpKoopa(x*16,y*16,(0,0,0),'jumpkoopa',[transform.flip(image.load("pics//jumpkoopa%s.png" %str(i)),True,False) for i in range(8)])
                    self.characters.append(enemy)

                if c == 15:
                    enemy = Lakitu(x*16,y*16,(0,0,0),'lakitu',[image.load("pics//lakitu%s.png" %str(i)) for i in range(9)])
                    self.characters.append(enemy)

                if c == 16:
                    enemy = Boo(x*16,y*16,[image.load("pics//boo%s.png" %str(i)) for i in range(3)])
                    self.characters.append(enemy)                        

                if c == 17:
                    enemy = Thwomp(x*16,y*16,[image.load("pics//thwimp%s.png" %str(i)) for i in range(3)],'thwimp')
                    self.characters.append(enemy)

                if c == 18:
                    enemy = Lavabubble(x*16,y*16,[image.load("pics//lavabubble%s.png" %str(i)) for i in range(6)],'lavabubble')
                    self.characters.append(enemy)

                if c == 20:
                    enemy = Thwomp(x*16,y*16,[image.load("pics//thwomp%s.png" %str(i)) for i in range(3)],'thwimp')
                    self.characters.append(enemy)

                if c == 22:
                    enemy = Bowser(x*16,y*16,[image.load("pics//bowserjr%s.png" %str(i)) for i in range(22)],'bowser')
                    self.characters.append(enemy)
                    


                    
##        self.player = Mario(200*16,21*16,(255,255,255),'mario')
##        self.player.hp = hp
##        self.player.lives = lives
##        self.characters.append(self.player)
        #self.characters.append(BulletBill(228*16,24*16,(0,0,0),'bulletbill',image.load("pics//cannon.png")))
        other = 1
        self.cam = Camera(complex_camera,self.SCREENX*32,self.SCREENY*32)
        
        while True:
            mx,my = mouse.get_pos()
            click = False
            
            for ev in event.get():
                if ev.type == QUIT:
                    quit()
                    return
                if ev.type == KEYDOWN:
                    if ev.key == K_SPACE:
                        game.main(2,self.player.hp)
                if ev.type == MOUSEBUTTONDOWN:
                    click = True
                        
            self.cam.update(game.player.rect)
            
            topscreen.blit(game.scene,(0,-127))
            topscreen.blit(self.base,self.cam.apply(self.base.get_rect()))
            btmscreen.blit(menu.back,(0,0))

            for ch in self.characters:
                ind = self.characters.index(ch)
                rect = game.cam.apply(Rect(ch.rect))
                if rect.x in range(-200,600) and rect.y in range(-200,340):
                    ch.update()
                    
                elif rect.x not in range(-200,600):
                    if ch.ch == 'bill':
                        del game.characters[ind]
                        
                    elif ch.ch == 'fireball':
                        del game.characters[ind]
                        
                if self.lvl.lvlnum == 1:
                    if ch.rect.y>432:
                        del self.characters[ind]
                        if ch.ch == 'mario': self.player.hp = 0
                        
                elif self.lvl.lvlnum == 2:
                    if ch.rect.y>588:
                        del self.characters[ind]
                        if ch.ch == 'mario': self.player.hp = 0
                elif self.lvl.lvlnum == 4:
                    if ch.rect.y>420:
                        if ch.ch == 'mario':
                            print(ch.rect.y)
                            self.player.hp = 0
                        #del self.characters[ind]
                        

            for tile in self.lvl.tiles:
                ind = self.lvl.tiles.index(tile)
                rect = self.cam.apply(tile.rect)
                topscreen.blit(tile.image,rect)
                tile.update()
                #SPecial tiles
                #Reqwuire different means of updating
                if tile.pos == 'temp':
                    tile.rect.y += 2*tile.up
                    if tile.image == tile.pics[-1]:
                        del self.lvl.tiles[ind]
                if tile.pos == 'starcoin':
                    if self.player.rect.colliderect(tile.rect):
                        tile.hit = True
                        self.starcount[tile.count] = 1
                        self.pts += 5000
                    if tile.hit:
                        tile.rect.y -= 4
                        tile.frame += 2
                        if rect.y>320:
                            del self.lvl.tiles[ind]
                if tile.pos == 'flag':
                    other = tile.rect.x
                    playrect = game.cam.apply(self.player.rect)
                    if playrect.x in range(rect.x,rect.x+3*16) and playrect.y in range(rect.y,rect.y+9*16):
                        self.player.finish(tile)
            #Updates inventory
            if self.item.ch != 'noitem':
                self.item.update()
                if self.item.rect.move(0,320).collidepoint((mx,my)) and click:
                    pics = [image.load("pics//fireflower%s.png" %str(i)) for i in range(3)]
                    powerup = PowerUp(self.player.rect.x,self.player.rect.y-100,(255,0,0),'fireflower',pics)
                    self.characters.append(powerup)
                    self.item.ch = 'noitem'
            #Fins position of starcoin
            for s in range(len(self.starcount)):
                if self.starcount[s] == 1:
                    btmscreen.blit(btmstar,starpos[s])
            #Updates btmscreen
            btmscreen.blit(arrow,(int(12+(self.player.rect.x/other)*427),75))
            btmscreen.blit(transform.scale(numimg[self.lvl.lvlnum],(14,27)),(123,21))
            btmscreen.blit(transform.scale(ptsimg[self.player.lives],(14,27)),(435,20))             
            
            if self.coincount == 100:
                self.player.lives += 1
                self.coincount = 0
                
            strcoin = '0'*(2-len(str(self.coincount)))+str(self.coincount)
            topscreen.blit(coinicon,(5,2))
            
            for i in range(len(strcoin)):
                pic = ptsimg[int(strcoin[i])]
                x = 35+10*i
                topscreen.blit(pic,(x,2))

                    
            strpts = '0'*(8-len(str(self.pts)))+str(self.pts)
            for p in range(len(strpts)):
                pic = ptsimg[int(strpts[p])]
                x = 105+10*p
                y = 210-p
                btmscreen.blit(pic,(x,y))
            
            screen.blit(topscreen,(0,0))
            screen.blit(btmscreen,(0,320))

            if mouse.get_pressed()[0] == 1:
                print(mouse.get_pos())
            #Death
            if self.player.hp == 0 or self.player not in self.characters:
                self.player.lives -= 1
                self.player.die()
                print("YOU DIED")
                if self.player.lives>0:
                    game.main(score=self.pts,coins=self.coincount,lives=self.player.lives,hp=1,lvl=self.lvl.lvlnum)
                else:
                    menu.loop()
                  
            self.clock.tick(35)
            display.flip()

class Menu:
    
    def __init__(self):
        self.back = image.load("bg0.png")
        self.icons = ['game','music','options','quit']
        self.pics = [transform.scale(image.load("menu pics//%s.png" %i),(90,90)) for i in self.icons]
        self.rects = [(140,60,90,90),(240,60,90,90),(140,160,90,90),(240,160,90,90)]
        self.ch = ''
        self.image = ''
        self.rect = ''

        self.back = image.load("btmbg0.png")
        self.bg = image.load("bg0.png")
     
    def grow(self):
        cover = Surface((480,320))
        x = 0
        cover.set_alpha(x)
        a,b = 1,1
        
        while True:
            
            btmscreen.blit(self.bg,(0,0))
            
            if self.ch == 'music':
                a,b = -1,1
            elif self.ch == 'options':
                a,b = 1,-1
            elif self.ch == 'quit':
                a,b = -1,-1
                
            if self.rect.x != int((btmscreen.get_width()-self.rect.width)/2): 
                self.rect = self.rect.move(a,b)
            else:
                x += 1
                cover.set_alpha(x)

            if x == 255: return
            
            btmscreen.blit(self.image,self.rect)
            btmscreen.blit(cover,(0,0))
            screen.blit(btmscreen,(0,320))

            display.flip()
            
    def transfer(self):
    
        if self.ch == 'game':
            self.ch = ''
            game.main(lvl = 6)
            
        if self.ch == 'music': pass

        if self.ch == 'options':
            self.optionmenu()

        if self.ch == 'quit':
            quit()

    def optionmenu(self):
        back = image.load("menu pics//optionsmenu.png")
        
        left = Rect(88,337,32,60)
        right = Rect(354,337,32,60)
        ok = Rect(214,593,50,40)
        bgarea = Rect(128,110,218,140)
        bg = [transform.scale(image.load("bg%s.png" %str(i)),(218,140)) for i in range(5)]

        current = 0
        ft = font.SysFont("Agency FB", 18)
        
        while True:
            mx,my = mouse.get_pos()
            mb = mouse.get_pressed()
            click = False
            
            for e in event.get():
                if e.type == MOUSEBUTTONDOWN:
                    print(e.pos)
                    if left.collidepoint((e.pos)):
                        current -= 1
                        if current == -1: current = 4
                    if right.collidepoint((e.pos)):
                        current += 1
                        if current == 5: current = 0
                    if ok.collidepoint((mx,my)):
                        self.back = image.load("btmbg%s.png" %str(current))
                        self.bg = image.load("bg%s.png" %str(current))
                        return
                    
            btmscreen.blit(self.bg,(0,0))
            label = ft.render(str(current+1), 1, (255,255,255))
            
            btmscreen.blit(back,(75,0))
            btmscreen.blit(bg[current],bgarea)
            btmscreen.blit(label,(274,35))
            
            screen.blit(btmscreen,(0,320))
            display.flip()
            
            
    def loop(self):
        counter = 0
        hit = False
        title = image.load("titlescreen.png")
        
        mixer.music.load(titlemus)
        mixer.music.play(-1)
        while True:

            mx,my = mouse.get_pos()
            mb = mouse.get_pressed()
            click = False
            
            for ev in event.get():
                if ev.type == QUIT:
                    running = False
                if ev.type == MOUSEBUTTONUP:
                    click = True
                    
            btmscreen.blit(self.bg,(0,0))
            
            if not hit:
                for i in range(len(self.pics)):

                    btmscreen.blit(self.pics[i],self.rects[i])
                    if Rect(self.rects[i]).move(0,320).collidepoint((mx,my)) and click:
                        self.image = self.pics[i]
                        self.rect = Rect(self.rects[i])
                        self.ch = self.icons[i]
                        hit = True
            
            if self.ch in self.icons and hit:                
                self.grow()
                self.transfer()
                self.ch = ''
                counter = 0

            counter = (counter+1)%30
            if counter == 0: hit = False
            topscreen.blit(title,(0,0)) 

            screen.blit(topscreen,(0,0))
            screen.blit(btmscreen,(0,320))
            display.flip()

def loadMap(fname):
    if fname in os.listdir("."):
        myPFile = open(fname, "rb")        # load my board that I pickled
        return pickle.load(myPFile)

def loadscreen(life):
    topscreen.fill((0,0,0))
    loading = image.load("pics//loadscreen.png")
    num = image.load("pics//num%s.png" %str(game.lvl.lvlnum))
    lives = image.load("pics//lives%s.png" %str(life))
    x = 255
    plus = 5
    cover = Surface((480,320))
    cover.set_alpha(x)

    mixer.music.load("mario music//music"+str(game.lvl.lvlnum)+".mid")
    while True:
        
        topscreen.fill((0,0,0))
        btmscreen.fill((0,0,0))
        x -= plus
        
        if x==0: plus *= -1
        if x == 255: return

        cover.set_alpha(x)
        
        topscreen.blit(loading,(0,0))
        topscreen.blit(num,(250,95))
        topscreen.blit(lives,(250,192))
        topscreen.blit(cover,(0,0))
        
        screen.blit(topscreen,(0,0))
        screen.blit(btmscreen,(0,320))
        
        display.flip()
                            
def deathscreen(gameover=False):
    death = Surface((480,320))
    
    done = image.load("pics//youdied.png")
    paste = (180,142)
    
    mixer.music.load("mario music//death.mid")
    
    
    if gameover:
        done = image.load("pics//gameover.png")
        paste = (148,142)
        mixer.music.load("mario music//Game Over.mid")
    cover = Surface((done.get_size()))

    
    
    x= 0
    a=255
    
    cover.set_alpha(a)
    death.set_alpha(x)

    mixer.music.play(1)
    
    while True:
        game.clock.tick(30)
        topscreen.blit(death,(0,0))
        btmscreen.blit(death,(0,0))
        if x<255:
            x += 4
            death.set_alpha(x)
        
        if x>=150 and a>0:
            a -= 5
            cover.set_alpha(a)
            topscreen.blit(done,paste)
            topscreen.blit(cover,paste)

        if a == 0:
            time.wait(100)
            return
        screen.blit(topscreen,(0,0))
        screen.blit(btmscreen,(0,320))
        display.flip()
        
def nintendo():
    nintendo = image.load("nintendo.png")
    cright = image.load("copyright.png")
    cover = Surface((480,320))
    cover.fill((255,255,255))
    x = 255
    
    while True:
        if x>0:
            x-= 5
        else: return

        cover.set_alpha(x)
        topscreen.blit(nintendo,(0,0))
        topscreen.blit(cover,(0,0))
        btmscreen.blit(cright,(0,0))
        btmscreen.blit(cover,(0,0))

        screen.blit(topscreen,(0,0))
        screen.blit(btmscreen,(0,320))
        display.flip()
     
screen = display.set_mode((480, 640),0,32)

topscreen = Surface((480,320),SRCALPHA)
btmscreen = Surface((480,320),SRCALPHA)

HALFWIDTH = screen.get_width()//2
HALFHEIGHT = screen.get_height()//2

mixer.init()

titlemus = 'mario music//Map.mid'

norm = 0
sup = 1
fire = 2

nintendo()

menu = Menu()
game = Game()

if __name__ == '__main__':
    
    init()
    
    menu.loop()
