import pygame
import random
import math
from pygame import mixer
pygame.init()
HS_FILE =  "highscore.txt"
from os import path

#screen size
screen = pygame.display.set_mode((800, 800))
backround = pygame.image.load('back.jpg')
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#music for the background
mixer.music.load('background.wav')
#mixer.music.play(-1)

#font for the score and gameover 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 16)
over_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#players ship
playerShip = pygame.image.load('falcon.png')
playerX = 400
playerY = 700
playerX_change = 0

#ufo 1
ufoIMG = []
ufo1X = []
ufo1Y = []
ufo1X_change  = []
ufo1Y_change = []
num_enemies = 10

#making a list of 6 enemies to fight
for i in range (num_enemies):
    ufoIMG.append(pygame.image.load('ufo.png'))
    ufo1X.append(random.randint(0, 800))
    ufo1Y.append(random.randint(50, 150))
    ufo1X_change.append(random.randint(1 ,10))
    ufo1Y_change.append(50)

#bullet 
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 700
bulletY_change = 20
bullet_state = "ready"

#score function
def score(x, y):
    scores = font.render("Score : " + str(score_value), 
    True, (255, 255,255))
    screen.blit(scores, (x, y))

#gameover function
def game_over():
    over = over_font.render("GAME OVER " , True, (255, 255, 255))
    screen.blit(over, (300, 350))

#player function
def player(x, y):
    screen.blit(playerShip, (x, y))

#enemy function
def ufo(x, y, i):
    screen.blit(ufoIMG[i], (x, y))

#bullet function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x + 16, y + 10))

#collition function
def collition(ufo1X, ufo1Y, bulletX, bulletY):
    distance = math.sqrt(math.pow(ufo1X - bulletX, 2) +
    math.pow(ufo1Y - bulletY, 2)) #does the math to see if there is a collition
    if distance < 27:
        boom = pygame.image.load('explosion.png') #explostion effect
        screen.blit(boom,(ufo1X, ufo1Y))
        return True
    else:
        return False

def load_data():
    dirt = path.dirname(__file__)
    with open(path.join(dirt, HS_FILE), 'r+') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0

#the game running loop
run = True
while run:
    #screen color, red green blue
    screen.fill((0, 0, 0)) 
    screen.blit(backround,(0, 0))
    load_data()
    #sets up the player controls and enters the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5 #movement  speed
            if event.key == pygame.K_RIGHT:
                playerX_change = 5 #movement speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletS = mixer.Sound('laser.wav')
                    bulletS.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY) #fires the bullet from the players cord
        
        #if player stops pressing a control the ship stops
        if event.type == pygame.KEYUP:
            if  event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  
                playerX_change = 0
    
    #checks the enemies to see if the strike the player, keeps track of what they are doing
    for i in range (num_enemies):
        if ufo1Y[i] > 700 and ufo1X[i] == (playerX + 10 or playerX - 10): #calls for gameover
            for j in range(num_enemies):
                ufo1Y[j] = 20000
                boom = pygame.image.load('explosion.png') #explostion effect
                screen.blit(boom,(playerX, playerY))
                playerX_change = 0

            game_over()
            break
        ufo1X[i] += ufo1X_change[i] #changes the enemy movement speed as they hit the walls
        if ufo1X[i] <= 0:
            ufo1X_change[i] = random.randint(1 ,10)
            ufo1Y[i] += ufo1Y_change[i]
        elif ufo1X[i]>= 736:
            ufo1X[i] = 736
            ufo1X_change[i] -= random.randint(1, 10)
            ufo1Y[i] += ufo1Y_change[i]
        
        #checks if the bullet his an enemy
        collitionT = collition(ufo1X[i], ufo1Y[i], bulletX, bulletY)
        if collitionT:
            boomS = mixer.Sound('boom.wav')
            boomS.play()
            bulletY = 700
            bullet_state = "ready"
            score_value += 1
            ufo1X[i] = random.randint(0, 800)
            ufo1Y[i] = random.randint(50, 150)
        ufo(ufo1X[i], ufo1Y[i], i)

    #creates a bullet
    if bulletY <= 0:
        bulletY = 700
        bullet_state = "ready"

    #allows bullet to move
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    #prevents player from leaving map
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    #updates that player location
    player(playerX, playerY)
    score(textX, textY)
    pygame.display.update()       