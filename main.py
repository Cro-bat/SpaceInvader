import pygame
import random

# Inicializar Pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load('astronave.png')
pygame.display.set_icon(icono)

# Jugador
playerImg = pygame.image.load('invasores-espaciales.png')
playerX = 370
playerY = 480
playerX_change = 0

# Ememigo
enemyImg = pygame.image.load('extraterrestre.png')
enemyX = random.randint(0, 800)
enemyY = 50
enemyX_change = 0.3
enemyY_change = 40


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


def enemy(x, y):
    screen.blit(enemyImg, (round(x), round(y)))


running = True
while running:

    # color de fondo RGB
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # Proceso de cierre
        if event.type == pygame.QUIT:
            running = False

        # Al presionar tecla revisar izq o der
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # Revisar limites de pantalla (jugador)
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Revisar limites de pantalla (enemigo)
    enemyX += enemyX_change
    if enemyX <= 0:
        enemyX_change = 0.1
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.1
        enemyY += enemyY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
