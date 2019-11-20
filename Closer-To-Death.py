#Game made by John Leomarc Alonzo/Jolealz/Vessalius
#Character Sprites - Amiel Manuel Ante, Justine Matthew Basa
#Game Audio - Gibson Diwa
import pygame
import os
pygame.init()

info = pygame.display.Info()

#Use this once you fix stuff
width = info.current_w
height = info.current_h

win = pygame.display.set_mode((1000,600))#, pygame.FULLSCREEN)

pygame.display.set_caption("Closer to Death")

walkRight = [pygame.image.load('R%s.png' % frame) for frame in range(1, 11)]
walkLeft = [pygame.image.load('L%s.png' % frame) for frame in range(1, 11)]
bg = pygame.image.load('bg.jpg')

bulletSound = ""#pygame.mixer.Sound('')
hitSound = ""
#bulletSound.play()
#music = pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play(-1)


clock = pygame.time.Clock()

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)# x y width height

    def draw(self, win):
        if self.walkCount + 1 >= 60:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//6], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//6], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)
                
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 0
        self.y = 520
        self.walkCount = 0
        diefont = pygame.font.SysFont("comicsans", 100)
        text = diefont.render('You Died.', 1, (255,0,0))
        win.blit(text, (500 - (text.get_width()/2), 300 - (text.get_height()/2)))
        pygame.display.update()
        i = 0
        while i < 100:#Delay for you died screen
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()
        pass

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R%sE.png' % frame) for frame in range(1, 11)]
    walkLeft = [pygame.image.load('L%sE.png' % frame) for frame in range(1, 11)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 8
        self.hitbox = (self.x + 17, self.y + 2, 32, 57)#Change this
        self.health = 10
        self.visible = True

    def draw(self,win):
        #Animation
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 60:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //6], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //6], (self.x, self.y))
                self.walkCount += 1

            #Health Bar
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,255,0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 5 * self.health, 10))

            self.hitbox = (self.x + 17, self.y + 2, 32, 57)#Change this
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            global score
            self.visible = False
            score += 20
        #print('Interaction detected.')
        pass


class item(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        
    def draw(self,win):
        if self.visible:
            pygame.draw.rect(win, (0,128,0), (self.x, self.y, self.width, self.height))
    
    def pickup(self):
        global score
        self.visible = False
        score += 20
        t = 0
        pickupfont = pygame.font.SysFont("comicsans", 30)
        text = pickupfont.render('+20', 1, (0,128,0))
        while t <= 25:
            win.blit(text, (140, 20))
            pygame.display.update()
            t += 1
        
        pass

class goal(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        
    def draw(self,win):
        if self.visible:
            pygame.draw.rect(win, (255,255,204), (self.x, self.y, self.width, self.height))
    
    def pickup(self):
        global score
        self.visible = False
        score += 20
        t = 0
        pickupfont = pygame.font.SysFont("comicsans", 200)
        text = pickupfont.render('You Win!!', 1, (255,255,204))
        while t <= 5000:
            win.blit(text, (500 - (text.get_width()/2), 300 - (text.get_height()/2)))
            pygame.display.update()
            t += 1
        
        pass



def redrawGameWindow():
    win.blit(bg, (0,0))
    text = scorefont.render('Score: ' + str(score), 1, (0,0,0)) #text antialias color
    win.blit(text, (20, 20))
    stage1.draw(win)
    points.draw(win)
    leo.draw(win)
    darkleo.draw(win)
    darkleo2.draw(win)
    darkleo3.draw(win)#Test
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()



scorefont = pygame.font.SysFont("comicsans", 30, True)


#mainloop
stage1 = goal(950, 0, 10, 580)
points = item(100, 550, 25, 25)
leo = player(0, 520, 64,64)
darkleo = enemy(70, 520, 64, 64, 900)
darkleo2 = enemy(300, 520, 64, 64, 700)
darkleo3 = enemy(500, 520, 64, 64, 700)#Test
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(60)
#----------------------------------------ITEM--------------------------------

            
    if points.visible == True:        
        if leo.hitbox[0] + leo.hitbox[2] > points.x and leo.hitbox[0] + leo.hitbox[2] < points.x + points.width: # SOMETHING YOU DID YEHEY
            if leo.hitbox[1] + leo.hitbox[3] > points.y and leo.hitbox[1] < points.y + points.height:
                points.pickup()
#---------------------------------------ITEM-------------------------------
                #Change the game here at stage1.pivkup()
#----------------------------------------STAGEGOAL--------------------------------

            
    if stage1.visible == True:        
        if leo.hitbox[0] + leo.hitbox[2] > stage1.x and leo.hitbox[0] + leo.hitbox[2] < stage1.x + stage1.width: # SOMETHING YOU DID YEHEY
            if leo.hitbox[1] + leo.hitbox[3] > stage1.y and leo.hitbox[1] < stage1.y + stage1.height:
                stage1.pickup()
                
                
                pygame.quit()
                os.system('CTD2.py') #TO RUN THE NEXT STAGE WOOO
#---------------------------------------STAGEGOAL-------------------------------
    
    
#-----------------------------------------------------------------darkleo------------------------    
    for bullet in bullets:
        if darkleo.visible == True:
            if bullet.y - bullet.radius < darkleo.hitbox[1] + darkleo.hitbox[3] and bullet.y + bullet.radius > darkleo.hitbox[1]:
                if bullet.x + bullet.radius > darkleo.hitbox[0] and bullet.x - bullet.radius < darkleo.hitbox[0] + darkleo.hitbox[2]:
                    #hitSound.play()
                    darkleo.hit()
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 1000 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    if darkleo.visible == True:        
        if leo.hitbox[0] + leo.hitbox[2] > darkleo.hitbox[0] and leo.hitbox[0] + leo.hitbox[2] < darkleo.hitbox[0] + darkleo.hitbox[2]: # SOMETHING YOU DID YEHEY
            if leo.hitbox[1] + leo.hitbox[3] > darkleo.hitbox[1] and leo.hitbox[1] < darkleo.hitbox[1] + darkleo.hitbox[3]:
                leo.hit()
                score -= 10
#----------------------------------------------darkleo-----------------------------------------------

#-----------------------------------------------------------------darkleo2------------------------    
    for bullet in bullets:
        if darkleo2.visible == True:
            if bullet.y - bullet.radius < darkleo2.hitbox[1] + darkleo2.hitbox[3] and bullet.y + bullet.radius > darkleo2.hitbox[1]:
                if bullet.x + bullet.radius > darkleo2.hitbox[0] and bullet.x - bullet.radius < darkleo2.hitbox[0] + darkleo2.hitbox[2]:
                    #hitSound.play()
                    darkleo2.hit()
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 1000 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    if darkleo2.visible == True:        
        if leo.hitbox[0] + leo.hitbox[2] > darkleo2.hitbox[0] and leo.hitbox[0] + leo.hitbox[2] < darkleo2.hitbox[0] + darkleo2.hitbox[2]: # SOMETHING YOU DID YEHEY
            if leo.hitbox[1] + leo.hitbox[3] > darkleo2.hitbox[1] and leo.hitbox[1] < darkleo2.hitbox[1] + darkleo2.hitbox[3]:
                leo.hit()
                score -= 10
#----------------------------------------------darkleo2-----------------------------------------------

#-----------------------------------------------------------------darkleo3------------------------    
    for bullet in bullets:
        if darkleo3.visible == True:
            if bullet.y - bullet.radius < darkleo3.hitbox[1] + darkleo3.hitbox[3] and bullet.y + bullet.radius > darkleo3.hitbox[1]:
                if bullet.x + bullet.radius > darkleo3.hitbox[0] and bullet.x - bullet.radius < darkleo3.hitbox[0] + darkleo3.hitbox[2]:
                    #hitSound.play()
                    darkleo3.hit()
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 1000 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    if darkleo3.visible == True:        
        if leo.hitbox[0] + leo.hitbox[2] > darkleo3.hitbox[0] and leo.hitbox[0] + leo.hitbox[2] < darkleo3.hitbox[0] + darkleo3.hitbox[2]: # SOMETHING YOU DID YEHEY
            if leo.hitbox[1] + leo.hitbox[3] > darkleo3.hitbox[1] and leo.hitbox[1] < darkleo3.hitbox[1] + darkleo3.hitbox[3]:
                leo.hit()
                score -= 10
#----------------------------------------------darkleo3-----------------------------------------------

#MOVEMENT
    keys = pygame.key.get_pressed()

    shootSpeed = 2 #Attack Speed
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > shootSpeed: #Attack Speed
        shootLoop = 0


    if keys[pygame.K_SPACE] and shootLoop == 0:
        #bulletSound.play()
        if leo.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 60:
            bullets.append(projectile(round(leo.x + leo.width //2), round(leo.y + leo.height//2), 6, (0,0,0), facing))

        shootLoop = 1

    if keys[pygame.K_a] and leo.x > leo.vel:
        leo.x -= leo.vel
        leo.left = True
        leo.right = False
        leo.standing = False
    elif keys[pygame.K_d] and leo.x < 1000 - leo.width - leo.vel:
        leo.x += leo.vel
        leo.right = True
        leo.left = False
        leo.standing = False
    else:
        leo.standing = True
        leo.walkCount = 0
        
    if not(leo.isJump):
        if keys[pygame.K_w]:
            leo.isJump = True
            leo.right = False
            leo.left = False
            leo.walkCount = 0
    else:
        if leo.jumpCount >= -10:
            neg = 1
            if leo.jumpCount < 0:
                neg = -1
            leo.y -= (leo.jumpCount ** 2) * .3 * neg
            leo.jumpCount -= 1
        else:
            leo.isJump = False
            leo.jumpCount = 10



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()

pygame.quit()
