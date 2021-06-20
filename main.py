import pygame
import random
import math
from pygame import mixer

# initialising pygame
pygame.init()

# creating gaming window
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Return of ultron")
icon = pygame.image.load("iron-man-vr.ico")
pygame.display.set_icon(icon)

# setting background image
background = pygame.image.load('download.jpg')
game_over = pygame.image.load('game_over.jpg')

# enemy
eyog=(410,200,300)#since we are changing y value of enemy later bt we need original value of y
ex=[750,750,750]#so that in the enemy part we dont need to repeat each code 3 different times
ey=[410,200,300]

enemy1 = pygame.image.load('ultron1.png')
def ultron1(x, y):
    screen.blit(enemy1, (x, y))


enemy2 = pygame.image.load('ultron2.png')
def ultron2(x, y):
    screen.blit(enemy2, (x, y))


enemy3 = pygame.image.load('ultron3.png')
e_x3 = ex[2]#jst to do parabola_y function
def ultron3(x, y):
    screen.blit(enemy3, (x, y))


def parabola_y(x0, x):
    return (420 - 1.2*((8 * (x - x0 + 150)) - ((4 / 75) * (x - x0 + 150) * (x - x0 + 150))))


# Player
ironman = pygame.image.load("iron.png")
ironx = 0
irony = 250
player_speed = 5#speed is for the rate at which x and y coordinates are changing.
def player():
    screen.blit(ironman, (ironx, irony))


# Laser
laserimg = pygame.image.load("laser.png")
laserx = 55
lasery = 270
laser_speed = 20
laser_state = 0
#state=0 means ready to fire
#state=1 means fired

#score
Score_count = 0
font = pygame.font.Font('Symtext.ttf',32)

strt_x = 10#x and y coordinate of the score to be displayed.
strt_y = 10

#bonus
def show_ptsbonus(Score_count):
    if (Score_count%10 == 0 or Score_count%10 == 2 or Score_count%10== 4) and (Score_count!=0 and Score_count!=2 and Score_count!=4) and game==1:
#so that this bonus is shown only after score is 10,12,14 and so on.
        ptsbonus=font.render("Points Bonus Activated",True,(0,0,255))
        screen.blit(ptsbonus,(300,50))

def show_laser_bonus():
    if (Score_count%10 == 0 or Score_count%10 == 2 or Score_count%10== 4) and (Score_count!=0 and Score_count!=2 and Score_count!=4) and game==1:
        laser_bonus=font.render("Laser Bonus Activated",True,(0,0,255))
        screen.blit(laser_bonus,(300,10))


def score_show(x,y):
    score = font.render("Score :"+str(Score_count),True,(255,0,0))
    screen.blit(score,(x,y))

def Calc_score(Score_count):
    if Score_count%10 == 0 or Score_count%10 == 2 or Score_count%10== 4 and Score_count>=10:
        return Score_count+2
    else:
        return Score_count+1

def bullet_speed(Score_count):
    if Score_count==0 or Score_count==2 or Score_count==4:
        laser_speed=20
    elif Score_count%10 == 0 or Score_count%10 == 2 or  Score_count%10 == 4 :
        laser_speed = 35
        show_laser_bonus()
    else:
        laser_speed = 20
    return laser_speed

def shoot(x, y):
    global laser_state
    laser_state = 1
    screen.blit(laserimg, (x + 55, y + 20))


def collision(laserx, lasery, ultronx, ultrony):
    dist = math.sqrt(math.pow(ultronx - laserx, 2) + math.pow(ultrony - lasery, 2))
    if dist < 50:
        return True
    return False

game=1
i=2 # i determines which of the 3 enemies are spawned
k = 0
clock = pygame.time.Clock()#create an object to help track time

#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# game loop
running = True
while running:
    flag=0# flag is to ensure that only one bullet is fired whenever collision occurs.
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    clock.tick(60)
    keys = pygame.key.get_pressed()#get the state of all keyboard buttons

    #Enemy spawn and movements
    if i==0 and game==1:
        ultron1(ex[i], ey[i])
        ex[i] -= 1 + (Score_count*0.05)

    elif i==1 and game==1:
        ultron2(ex[i], ey[i])
        ex[i] -= 1 + (Score_count*0.05)
        k += 1
        if k == 100:
            k = 0
            ey[i] = 10*random.randint(20, 40)
    elif i==2 and game==1:
        ultron3(ex[i], ey[i])
        ex[i] -= 1 + (Score_count*0.05)
        if ey[i] <= 420:
            ey[i] = parabola_y(e_x3, ex[i])
        else:
            e_x3 = ex[i]
            ey[i] = parabola_y(e_x3, ex[i])

    #Player movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_LEFT] and ironx - player_speed > 0 and game==1:
        ironx -= player_speed
    if keys[pygame.K_RIGHT] and ironx + player_speed < 300 and game==1:
        ironx += player_speed
    if keys[pygame.K_UP] and irony - player_speed > 0 and game==1:
        irony -= player_speed
    if keys[pygame.K_DOWN] and irony + player_speed < 450 and game==1:
        irony += player_speed
    if keys[pygame.K_SPACE] and laser_state==0 and flag==0 and game==1:
            laserx = ironx
            lasery = irony
            flag=0
            shoot(laserx, lasery)
    if game==0 and keys[pygame.K_r]:#to restart the game after game is over.
        game=1
        screen.blit(background,(0,0))
        ex[i]=750
        Score_count=0
                

    if laserx >= 800:#to restrict laser/missile
        laserx = 55
        laser_state = 0

    if laser_state == 1:
        shoot(laserx, lasery)
        laserx += laser_speed

    #Game over
    if collision(ironx,irony,ex[i],ey[i]) is True or ex[i]<=0 :
        endfont=pygame.font.Font('Symtext.ttf',64)
        screen.blit(game_over,(0,0))
        game=0
        
    #collision
    if collision(laserx,lasery,ex[i],ey[i]+10) is True and laser_state==1:
        mixer.music.load('explosion.wav')
        mixer.music.play(0)
        laserx =55
        laser_state = 0
        flag=1
        Score_count = Calc_score(Score_count)
        i=random.randint(0,2) #Spawn new enemy 
        ex[i] = 750
        ey[i] = eyog[i]

    if game==1:
        player()

    score_show(strt_x,strt_y)
    show_laser_bonus()
    show_ptsbonus(Score_count)

    pygame.display.update()  # to update screen regularly