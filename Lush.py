import pygame
import random
import math
import os
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode([700, 500])
caption = pygame.display.set_caption('Lush')

#fonts
font_s32 = pygame.font.Font('Malkor-Bold.ttf', 32)
font_s40 = pygame.font.Font('Malkor-Bold.ttf', 40)
font_s72 = pygame.font.Font('Malkor-Bold.ttf', 72)

# high score
highscore_record = 'Last high score created by: '
new_highscore_created = 'NEW HIGH SCORE CREATED!'
recordX = 150
recordY = 275
# value
if os.path.exists('high score.txt'):
    with open('high score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# creator
if os.path.exists('high score creator.txt'):
    with open('high score creator.txt', 'r') as file:
        highscore_creator = file.read()
else:
    highscore_creator = ''

# Background sound
background_sound = mixer.Sound('Game-music.wav')

# instructions
instructions_str1 = 'Press S to start'
instructions_str2 = 'Press SPACE BAR to jump over obstacles'
instructions_str3 = 'AVOID'
instructions_str4 = 'COLLECT                   for Bonus'
instructions_str5 = 'Press R to replay'
instructionsX = 40
instructionY1 = 100
instructionY2 = 200
instructionY3 = 300
instructionY4 = 400
instructionX5 = 475 
instructionY5 = 450
instruction1Img = pygame.image.load('AVOID instruction.png')
instruction1_imageX = 200
instruction1_imageY = 250
instruction2Img = pygame.image.load('COLLECT instructions.png')
instruction2_imageX = 215
instruction2_imageY = 400
        
# static background
static_background_1Img = pygame.image.load('blue background final.jpg')
static_background_1X = 0
static_background_1Y = 0
static_background_1X_change = 0
static_background_1_state = 'static'
overall_background_state = 'static'

# player
playerImg = pygame.image.load('Main Character.png')
playerX = 0
playerY = 350
playerX_change = 0
playerY_change = 0

# score
score_val = 0
score_textX = 10
score_textY = 10

# game over
gameover_textX = 100
gameover_textY = 200
gameover = False
gameover_sound_stop = False

# obstacles
'''
Red obstacle 64 pixels : Y : 350
Purple obstacle : Y : 350
Barrel obstacle : Y : 325
Fire obstacle : Y : 375
'''
# obstacle 1
obstacle1Img = pygame.image.load('Red obstacle 64 pixels.png')
obstacle1X = random.randrange(1000, 1500)
obstacle1Y = 350
obstacle1X_change = -0.5
obstacle1_state = 'static'
# obstacle 2
obstacle2Img = pygame.image.load('Purple obstacle.png')
obstacle2X = random.randrange(1500, 2000)
obstacle2Y = 350
obstacle2X_change = -0.5
obstacle2_state = 'static'
# obstacle 3
obstacle3Img = pygame.image.load('Barrel obstacle.png')
obstacle3X = random.randrange(2000, 2500)
obstacle3Y = 325
obstacle3X_change = -0.5
obstacle3_state = 'static'
# obstacle 4
obstacle4Img = pygame.image.load('Fire obstacle.png')
obstacle4X = random.randrange(2500, 3000)
obstacle4Y = 375
obstacle4X_change = -0.5
obstacle4_state = 'static'

# bonus coins
coinImg = pygame.image.load('coin.png')
coinX = random.randrange(1500, 3000)
coinY = random.randrange(250, 380)
coinX_change = -0.5
coin_state = 'moving'

def show_highscore(x, y):
    if score_val//2500 < high_score:
        highscore = font_s32.render(highscore_record + highscore_creator,True, (225,225,225))
        screen.blit(highscore, (x, y))
    else:
        highscore = font_s32.render(new_highscore_created, True, (225, 225, 225))
        screen.blit(highscore, (x, y))

def instruction1(x, y):
    ins1 = font_s32.render(instructions_str1, True, (225, 225, 225))
    screen.blit(ins1, (x, y))

def instruction2(x, y):
    ins2 = font_s32.render(instructions_str2, True, (225, 225, 225))
    screen.blit(ins2, (x, y))

def instruction3(x, y):
    ins3 = font_s32.render(instructions_str3, True, (225, 225, 225))
    screen.blit(ins3, (x, y))

def instruction4(x, y):
    ins4 = font_s32.render(instructions_str4, True, (225, 225, 225))
    screen.blit(ins4, (x, y))

def instruction5(x, y):
    ins5 = font_s32.render(instructions_str5, True, (225, 225, 225))
    screen.blit(ins5, (x, y))

def instruction_image1(x, y):
    screen.blit(instruction1Img, (x, y))

def instruction_image2(x, y):
    screen.blit(instruction2Img, (x, y))

def static_background_1(x, y):
    global static_background_1_state
    static_background_1_state = 'moving'
    screen.blit(static_background_1Img, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def show_score(x, y):
    score = font_s40.render('Score: '+ str(score_val//2500),True, (225,225,225))
    screen.blit(score, (x, y))

def gameover_display(x, y):
    end_txt = font_s72.render('G A M E   O V E R !', True, (225, 225, 225))
    screen.blit(end_txt, (x, y))

def obstacle1(x, y):
    global obstacle1_state
    obstacle1_state = 'moving'
    screen.blit(obstacle1Img, (x, y))

def obstacle2(x, y):
    global obstacle2_state
    obstacle2_state = 'moving'
    screen.blit(obstacle2Img, (x, y))

def obstacle3(x, y):
    global obstacle3_state
    obstacle3_state = 'moving'
    screen.blit(obstacle3Img, (x, y))

def obstacle4(x, y):
    global obstacle4_state
    obstacle4_state = 'moving'
    screen.blit(obstacle4Img, (x, y))

def iscollision1(playerX, playerY, obstacle1X, obstacle1Y):
    distance1 = math.sqrt(math.pow(playerX - obstacle1X, 2) + math.pow(playerY - obstacle1Y, 2))
    if distance1 < 30:
        return True
    else:
        return False

def iscollision2(playerX, playerY, obstacle2X, obstacle2Y):
    distance2 = math.sqrt(math.pow(playerX - obstacle2X, 2) + math.pow(playerY - obstacle2Y, 2))
    if distance2 < 30:
        return True
    else:
        return False

def iscollision3(playerX, playerY, obstacle3X, obstacle3Y):
    distance3 = math.sqrt(math.pow(playerX - obstacle3X, 2) + math.pow(playerY - obstacle3Y, 2))
    if distance3 < 30:
        return True
    else:
        return False

def iscollision4(playerX, playerY, obstacle4X, obstacle4Y):
    distance4 = math.sqrt(math.pow(playerX - obstacle4X, 2) + math.pow(playerY - obstacle4Y, 2))
    if distance4 < 30:
        return True
    else:
        return False

def coin(x, y):
    global coin_state
    coin_state = 'moving'
    screen.blit(coinImg, (x, y))

def isbonus(playerX, playerY, coinX, coinY):
    distance_coin = math.sqrt(math.pow(playerX - coinX, 2) + math.pow(playerY - coinY, 2))
    if distance_coin < 35:
        return True 
    else:
        return False

run = True
while run:

    if gameover:
        background_sound.stop()
        playerX_change = 0
        playerY_change = 0
        static_background_1X_change = 0
        obstacle1X_change = 0
        obstacle2X_change = 0
        obstacle3X_change = 0
        obstacle4X_change = 0
        overall_background_state = 'static'
        coinX_change = 0

        if gameover_sound_stop == False:
            gameover_sound = mixer.Sound('Game over sound.wav')
            gameover_sound.play()
            gameover_sound_stop = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                        gameover = False
                        gameover_sound.stop()
                        # Reinitialising variables
                        static_background_1Img = pygame.image.load('blue background final.jpg')
                        static_background_1X = 0
                        static_background_1Y = 0
                        static_background_1X_change = 0
                        static_background_1_state = 'static'
                        overall_background_state = 'static'
                        playerImg = pygame.image.load('Main Character.png')
                        playerX = 0
                        playerY = 350
                        playerX_change = 0
                        playerY_change = 0
                        score_val = 0
                        font_s40 = pygame.font.Font('Malkor-Bold.ttf', 40)
                        score_textX = 10
                        score_textY = 10
                        font_s72 = pygame.font.Font('Malkor-Bold.ttf', 72)
                        gameover_textX = 100
                        gameover_textY = 200
                        gameover = False
                        gameover_sound_stop = False
                        obstacle1Img = pygame.image.load('Red obstacle 64 pixels.png')
                        obstacle1X = random.randrange(1000, 1500)
                        obstacle1Y = 350
                        obstacle1X_change = -0.5
                        obstacle1_state = 'static'
                        obstacle2Img = pygame.image.load('Purple obstacle.png')
                        obstacle2X = random.randrange(1500, 2000)
                        obstacle2Y = 350
                        obstacle2X_change = -0.5
                        obstacle2_state = 'static'
                        obstacle3Img = pygame.image.load('Barrel obstacle.png')
                        obstacle3X = random.randrange(2000, 2500)
                        obstacle3Y = 325
                        obstacle3X_change = -0.5
                        obstacle3_state = 'static'
                        obstacle4Img = pygame.image.load('Fire obstacle.png')
                        obstacle4X = random.randrange(2500, 3000)
                        obstacle4Y = 375
                        obstacle4X_change = -0.5
                        obstacle4_state = 'static'
                        coinImg = pygame.image.load('coin.png')
                        coinX = random.randrange(1500, 3000)
                        coinY = random.randrange(250, 380)
                        coinX_change = -0.5
                        coin_state = 'moving'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    gameover = False
        # high score update
        if score_val//2500 > high_score:
            high_score = score_val//2500
            with open('high score.txt', 'w') as file:
                file.write(str(high_score))
            with open('high score creator.txt', 'r') as file:
                highscore_creator = file.read()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                overall_background_state = 'moving'
                playerX_change = 1.5
                static_background_1X_change = 0.5
            if overall_background_state == 'moving':
                if event.key == pygame.K_SPACE:
                    if playerY >= 350:
                        playerY_change = -0.75

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                overall_background_state = 'moving'
                playerX_change = 1.5
                static_background_1X_change = 0.5
            if overall_background_state == 'moving':
                if event.key == pygame.K_SPACE:
                    playerY_change = 0.75

    # Collisions
    collision1 = iscollision1(playerX, playerY, obstacle1X, obstacle1Y)
    collision2 = iscollision2(playerX, playerY, obstacle2X, obstacle2Y)
    collision3 = iscollision3(playerX, playerY, obstacle3X, obstacle3Y)
    collision4 = iscollision4(playerX, playerY, obstacle4X, obstacle4Y)
    gameover = collision1 or collision2 or collision3 or collision4
    
    if not gameover:
        background_sound.play()
        if playerY < 200:
            playerY_change = 0.7
        if playerY > 350:
            playerY = 350
        if playerX > 225:
            playerX_change = 0

            # obstacle movements
            # obstacle 1
            if obstacle1X <= -65:
                obstacle1X = random.randrange(1000, 1500)
                obstacle1_state = 'static'
            if obstacle1_state == 'moving':
                obstacle1(obstacle1X, obstacle1Y)
                obstacle1X += obstacle1X_change
            # obstacle 2
            if obstacle2X <= -65:
                obstacle2X = random.randrange(1500, 2000)
                obstacle2_state = 'static'
            if obstacle2_state == 'moving':
                obstacle2(obstacle2X, obstacle2Y)
                obstacle2X += obstacle2X_change
            if -75 < obstacle1X - obstacle2X < 75:
                obstacle2X += 100
            # obstacle 3
            if obstacle3X <= -65:
                obstacle3X = random.randrange(2000, 2500)
                obstacle3_state = 'static'
            if obstacle3_state == 'moving':
                obstacle3(obstacle3X, obstacle3Y)
                obstacle3X_change += obstacle3X_change
            if -75 < obstacle1X - obstacle3X < 75:
                obstacle3X += 100
            if -75 < obstacle2X - obstacle3X < 75:
                obstacle3X += 100
            # obstacle 4
            if obstacle4X <= -65:
                obstacle4X = random.randrange(2500, 3000)
                obstacle4_state = 'static'
            if obstacle4_state == 'moving':
                obstacle4(obstacle4X, obstacle4Y)
                obstacle4X += obstacle4X_change
            if -75 < obstacle1X - obstacle4X < 75:
                obstacle4X += 100
            if -75 < obstacle2X - obstacle4X < 75:
                obstacle4X += 100
            if -75 < obstacle3X - obstacle4X < 75:
                obstacle4X += 100

            # coin movement
            if coinX <= -20:
                coinX = random.randrange(1500, 3000)
                coinY = random.randrange(250, 380)
                coin_state = 'static'
            if coin_state == 'moving':
                coin(coinX, coinY)
                coinX += coinX_change

        # background movement
        if overall_background_state == 'moving':
            static_background_1X -= static_background_1X_change
            score_val += 1

        if static_background_1X < -14000: # 6300 for red; 14000 for blue
            static_background_1X = 0
        
        # bonus
        bonus = isbonus(playerX, playerY, coinX, coinY)
        if bonus:
            score_val += 26000
            coinX = random.randrange(1500, 3000)
            coinY = random.randrange(250, 380)

    playerX += playerX_change
    playerY += playerY_change

    static_background_1(static_background_1X, static_background_1Y)
    show_score(score_textX, score_textY)
    coin(coinX, coinY)
    obstacle1(obstacle1X, obstacle1Y)
    obstacle2(obstacle2X, obstacle2Y)
    obstacle3(obstacle3X, obstacle3Y)
    obstacle4(obstacle4X, obstacle4Y)
    player(playerX, playerY)
    if gameover:
        show_highscore(recordX, recordY)
        gameover_display(gameover_textX, gameover_textY)
        instruction5(instructionX5, instructionY5)
        mixer.music.stop()
    if overall_background_state == 'static' and not gameover:
        instruction1(instructionsX, instructionY1)
        instruction2(instructionsX, instructionY2)
        instruction3(instructionsX, instructionY3)
        instruction4(instructionsX, instructionY4)
        instruction_image1(instruction1_imageX, instruction1_imageY)
        instruction_image2(instruction2_imageX, instruction2_imageY)
    pygame.display.update()