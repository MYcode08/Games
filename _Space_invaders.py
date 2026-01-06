import pygame
from pygame import mixer # Load the mixer module for sound
import random
import math  

# Intialize Pygame
pygame.init()
clock = pygame.time.Clock() 

# Set up the display
screen = pygame.display.set_mode((800, 600))

#Background 
background = pygame.image.load('Space.jpg')  # Ensure you have a background image named "Space.jpg"

#background sound
mixer.music.load('background.wav')  # Ensure you have a background sound named "background.wav"
mixer.music.play(-1)  # Play the background sound on a loop

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')  # Ensure you have an icon image named "ufo.png"
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('spaceship.png')  # Ensure you have a player image named "spaceship.png"
playerX = 370
playerY = 480
playerX_change = 0

#alien 
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 6

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('alien.png'))  # Ensure you have an enemy image named "enemy.png"
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(50, 150))
    alienX_change.append(0.4)
    alienY_change.append(40)

#sword 
swordImg = pygame.image.load('sword.png')  # Ensure you have an enemy image named "enemy.png"
swordX = 0
swordY = 480 
swordX_change = 0
swordY_change = 10 
sword_state = "ready"  # "ready" - You can't see the sword on the screen
                      # "fire" - The sword is currently moving

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # Ensure you have a font named "freesansbold.ttf"
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y)) # Draw the player at its current position

def alien(x,y,i):
    screen.blit(alienImg[i], (x, y)) # Draw the alien at its current position

def fire_sword(x,y):
    global sword_state
    sword_state = "fire"
    screen.blit(swordImg, (x + 16, y + 10)) # Draw the sword at its current position

def isCollision(alienX, alienY, swordX, swordY):
    distance = math.sqrt((math.pow(alienX - swordX, 2)) + (math.pow(alienY - swordY, 2)))
    if distance < 27:
        return True
    else: 
        return False
    
def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250)) 

#Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Fill the screen with black
    screen.blit(background, (0, 0))  # Draw the background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # if key pressed check whether its right or left 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if sword_state is "ready": # Check if sword is ready to be fired
                    sword_sound = mixer.Sound('laser.wav')  # Ensure you have a sound named "laser.wav"
                    sword_sound.play()
                    swordX = playerX
                    fire_sword(swordX, swordY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736 

    #Alien Movement 
    for i in range(num_of_aliens):

        #Game Over
        if alienY[i] > 430:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i] 
        if alienX[i] <= 0:
            alienX_change[i] = 0.4
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.4
            alienY[i] += alienY_change[i]
        
        #Collision
        collision = isCollision(alienX[i], alienY[i], swordX, swordY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            swordY = 480
            sword_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(50, 150)
        
        alien(alienX[i], alienY[i], i)  # Draw the alien

    #Sword Movement
    if swordY <= 0:
        swordY = 480
        sword_state = "ready"
    if sword_state is "fire":
        fire_sword(swordX, swordY)
        swordY -= swordY_change

    player(playerX,playerY)  # Draw the player
    show_score(textX, textY)  # Show the score 
    pygame.display.update()  # Update the display