import pygame
from pygame import mixer
import math
import random

pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))
running = True
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)


#bachground
bg = pygame.image.load("stars.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)
# Score
score_val = 0
font = pygame.font.Font("leaves_and_ground.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_val), True, (255, 255, 255))
    screen.blit(score,(x,y))

# Enemy
enemyImg = []
EnemyX = []
EnemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    EnemyX.append(random.randint(64, 736))
    EnemyY.append(random.randint(50, 150))
    enemyX_change.append(.3)
    enemyY_change.append(40)

# Player
playerImg = pygame.image.load("spaceship.png")

PlayerX = 370
PlayerY = 480

player_change = 0

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = PlayerX
bulletY = 480
bullet_state = "ready"  # ready = you can't see the bullet unless it is fired(fire state)
bulletX_change = 0
bulletY_change = 1

#game over text
font = pygame.font.Font("leaves_and_ground.ttf", 64)
def game_over():

    over = font.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (200, 250))


# collision
def isColllision(EnemyX, bulletX, EnemyY, bulletY):
    distance = math.sqrt((math.pow((EnemyX - bulletX), 2)) + (math.pow((EnemyY - bulletY), 2)))
    if distance < 27 and EnemyY < (PlayerY - 32):
        explosion_Sound = mixer.Sound("explosion.wav")
        explosion_Sound.play()
        return True
    else:
        return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y - 15))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = - 0.5
            if event.key == pygame.K_RIGHT:
                player_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = PlayerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_change = 0

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    EnemyX += enemyX_change

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    for i in range(no_of_enemies):
        #Game Over
        if EnemyY[i]>440:
            for j in range(no_of_enemies):
                EnemyY[j] =2000
            game_over()
        EnemyX[i] += enemyX_change[i]
        if EnemyX[i] >= 736:
            enemyX_change[i] = -0.3
            EnemyY[i] += enemyY_change[i]
        if EnemyX[i] < 0:
            enemyX_change[i] = 0.3
            EnemyX[i] += enemyY_change[i]

        # collision
        collision = isColllision(EnemyX[i], bulletX, EnemyY[i], bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            EnemyX[i] = random.randint(64, 735)
            EnemyY[i] = random.randint(50, 150)

        enemy(EnemyX[i], EnemyY[i], i)

    if PlayerX < 0:
        PlayerX = 800
    PlayerX += player_change
    if PlayerX >= 736:
        PlayerX = 736
    if PlayerX <= 0:
        PlayerX = 0
    player(PlayerX, PlayerY)
    show_score(textX, textY)
    pygame.display.update()
