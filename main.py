import pygame  # loading the pygame library
import random
import math

from pygame import mixer

# initiaize the pygame
pygame.init()  # we use init to initialize pygame library

# creating the screen
screen = pygame.display.set_mode((800, 600))  # always make sure to contain the hight and width inside a tuple

# Title and icon
pygame.display.set_caption("Space invaders")  # setting the display name
icon = pygame.image.load('spaceship.png')  # loading the path
pygame.display.set_icon(icon)  # setting the icon from the icon path

# background image

background = pygame.image.load('space-bg.jpg')

# background sound

mixer.music.load('background.wav')
mixer.music.play(-1)

# player image

playerimg = pygame.image.load('space-invaders.png')
playerX = 368  # X coordinate of the player
playerY = 480  # Y coordinate of the player
playerX_change = 0

# enemy image
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('virus.png'))
    enemyX.append(random.randint(0, 736))  # X coordinate of the player
    enemyY.append(random.randint(50, 150))  # Y coordinate of the player
    enemyX_change.append(2)
    enemyY_change.append(20)

# bullet image

bulletimg = pygame.image.load('bullet.png')
bulletY = 480  # Y coordinate of the player
bulletX = 0
bulletY_change = 5
bullet_state = 'ready'  # ready means the bullet is ready to fire and 'fire' means it is fired

# score

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf',64)
textX = 10
textY = 10

# game over text

def game_over_text():
    over_text = game_over_font.render("GAME OVER!!!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



def show_score(x, y):
    scoreprint = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreprint, (x, y))


# creating player function

def player(x, y):
    screen.blit(playerimg, (x, y))


# creating enemy function

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


# creating bullet firing function:

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))


# collision function

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    return False


# Game loop

running = True  # setting the running value as true
while running:
    # screen color
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    # checking if Quit is press or not
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed check right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # changing the X and Y coordinate of the player and the enemy
    playerX += playerX_change
    enemyX += enemyX_change

    # creating a boundary for the player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy boundries

    for i in range(num_of_enemies):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

            # collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # calling the player
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # to update the display
