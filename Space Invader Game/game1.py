import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen of game
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('Background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 shows as a loop which create music always


# Title and Icon of Window
pygame.display.set_caption("Space Invaders")  # Title
icon = pygame.image.load('icon.png')  # icon loading
pygame.display.set_icon(icon)  # display the icon  



# Space Ship
shipImage = pygame.image.load('ship.png')
shipX = 370
shipY = 510
shipX_change = 0


# Enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemy = 7

for i in range(num_of_enemy):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735)) 
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(5)
    enemyY_change.append(40)


# Bullet
   #ready => You can't see the bullet on the screen
   #   fire => The bullet is currently moving 
bulletImage = pygame.image.load('bullet.png')
bulletX = 0 
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255,255,255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render('Score :'+str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def ship(x, y):
    screen.blit(shipImage, (x, y)) # To Draw a ship image     blit means draw

def enemy(x, y , i):
    screen.blit(enemyImage[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImage, (x+10, y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True 
while running:
    # RGB => Red, Blue, Green
    screen.fill((0,0,0))
    
    # background
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        # If Keystroke is pressed chechk whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shipX_change = -5
            if event.key == pygame.K_RIGHT:
                shipX_change = 5

            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = shipX
                fire_bullet(shipX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                shipX_change = 0

    # Checking for boundaries of space ship
    shipX += shipX_change
    if shipX >= 738:
        shipX = 738 
    elif shipX <= 0:
        shipX = 0 
    
    # Checking for boundaries of enemy
    # Movement of enemeies
    for i in range(num_of_enemy):

        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[i] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 738:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]


         # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735) 
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
    

    # Bullet Movement
    if bulletY == 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    ship(shipX, shipY)

    show_score(textX, textY)
   
    pygame.display.update()


    
 
