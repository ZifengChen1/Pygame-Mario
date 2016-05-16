from pygame import *
from mariotry import *

class Menu:

    def loop(self):
        option = 0

        self.back = image.load("pics//menuback.png")
        title = image.load("pics//selectgame.png")

        greenpipe = image.load("pics//menupipe.png")
        bluepipe = image.load("pics//bluepipe.png")
        
        selectgreen = image.load("pics//menuselectpipe.png")
        selectblue = image.load("pics//selectblue.png")

        selectgame = image.load("pics//gameselect.png")
        newgame = image.load("pics//newgame.png")
        selectoption = image.load("pics//optionsselect.png")
        newoption = image.load("pics//newoptions.png")
                               
        w,h = self.back.get_size()
        tw,th = 480/w,320/h

        others = [selectgreen, selectblue, selectgame, selectoption]

        pos = [(0,0),(0,0),(170,113), (170,213),(105,100),(105,200)]
        pics = [menu.back, title, newgame, newoption, greenpipe, bluepipe]
        rects = [0 for i in range(len(pics))]
        
        for i in range(len(pics)):
            width,height = pics[i].get_size()
            pics[i] = transform.scale(pics[i],(int(width*tw),int(height*th)))
            rects[i] = Rect(pos[i],pics[i].get_size())

        for i in range(len(others)):
            width,height = others[i].get_size()
            others[i] = transform.scale(others[i],(int(width*tw),int(height*th)))

        while True:
            for ev in event.get():
                if ev.type == QUIT:
                    quit()
                    return
            keydown = False
            
            keys = key.get_pressed()                 
            mx,my = mouse.get_pos()

            if keys[K_DOWN] and option<1:
                option += 1
            elif keys[K_UP] and option>0:
                option -= 1
                
            for i in range(len(pics)):
                btmscreen.blit(pics[i],pos[i])                
                if option == 0:
                    btmscreen.blit(pics[3],pos[3])
                    if keys[K_KP_ENTER]: return
                    if i == 4:
                        btmscreen.blit(pics[0].subsurface(rects[i]),rects[i])
                        btmscreen.blit(others[0],(60,100))
                        btmscreen.blit(others[2],(125,113))
                    
                elif option == 1:
                    btmscreen.blit(pics[2],pos[2])
                    if i == 5:
                        btmscreen.blit(pics[0].subsurface(rects[i]),rects[i])
                        btmscreen.blit(others[1],(60,200))
                        btmscreen.blit(others[3],(125,213))
            screen.blit(btmscreen,(0,320))        
                    
            display.flip()
game = Game()
if __name__ == '__main__':
    init()
    menu = Menu()
    menu.loop()
    
    game.main()
