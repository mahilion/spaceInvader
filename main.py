import pygame
import random
import math
from pygame import mixer

# initialise the pygame
pygame.init()

# screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mahilion Space Invader")
icon = pygame.image.load("lion.png")
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
pygame.display.set_icon(icon)
backgroundImg = pygame.image.load("background-new.png")

# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerXChange = 0

enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("planet.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(0.3)
    enemyYChange.append(25)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 5
bullet_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance <= 27:
        return True
    else:
        return False


# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 350
scoreY = 550


def showScore(x, y):
    scoreRender = font.render("Score:" + str(score), True, (255, 255, 255))
    screen.blit(scoreRender, (x, y))


gameOverFont = pygame.font.Font('freesansbold.ttf', 64)


def gameOver():
    overRender = gameOverFont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(overRender, (200, 250))


running = True

# game loop
while running:

    # background colour
    screen.fill((0, 0, 0))
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChange = -1
            if event.key == pygame.K_RIGHT:
                playerXChange = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChange = 0

    # Player movement
    playerX += playerXChange
    # Check for boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        if enemyY[i] > 300:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
            enemyXChange[i] = 0.3
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] >= 736:
            enemyX[i] = 736
            enemyXChange[i] = -0.3
            enemyY[i] += enemyYChange[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()
            score += 1
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(i, enemyX[i], enemyY[i])

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)
    showScore(scoreX, scoreY)
    # update screen in game loop to see the changes
    pygame.display.update()
