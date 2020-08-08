import math
import pygame

# Inicializar Pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode((800, 600))

# Musica de fondo
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

# Fondo
# background = pygame.image.load('background.png')

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
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyIncrement = []
num_of_enemies = 6

conteo_spawn = 1


def spawn_enemy():
    global conteo_spawn
    enemyImg.append(pygame.image.load('extraterrestre.png'))
    enemyX.append(64 * conteo_spawn)
    conteo_spawn += 2

    if conteo_spawn > 10:
        conteo_spawn = 1

    enemyY.append(64)
    enemyX_change.append(0.3)
    enemyY_change.append(64)
    enemyIncrement.append(1)


for i in range(num_of_enemies):
    spawn_enemy()

# Bala - No se puede ver en pantalla hasta disparar
bulletImg = pygame.image.load('bala.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2
bullet_state = "ready"

# Puntuación

score_value = 0
font = pygame.font.Font('PixelFJVerdana12pt.ttf', 24)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('PixelFJVerdana12pt.ttf', 32)


def player(x, y):
    screen.blit(playerImg, (round(x), round(y)))


def enemy(x, y, index):
    screen.blit(enemyImg[index], (round(x), round(y)))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (int(x + 16), int(y + 10)))


def iscollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))
    pygame.mixer.music.set_volume(0)


# Loop de juego
running = True
while running:

    # color de fondo RGB
    screen.fill((0, 0, 0))
    # Imagen de fondo
    # screen.blit(background, (0,0))

    for event in pygame.event.get():
        # Proceso de cierre
        if event.type == pygame.QUIT:
            running = False

        # Al presionar tecla revisar izq o der
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Obtener cordenada en X de la nave
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)

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
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3 * enemyIncrement[i]
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3 * enemyIncrement[i]
            enemyY[i] += enemyY_change[i]
            enemyIncrement[i] += .2

        score_before = score_value

        # Colision
        collision = iscollision(enemyX[i], bulletX, enemyY[i], bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = 64 * conteo_spawn
            enemyY[i] = 64
            enemyIncrement[i] = 1

        score_now = score_value

        if score_value % 10 == 0 and score_value != 0 and score_value - score_before != 0:
            num_of_enemies += 1
            spawn_enemy()

        enemy(enemyX[i], enemyY[i], i)

    # Movimiento de bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
