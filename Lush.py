import pygame
import random
import math
from datetime import datetime
from pygame import mixer
import mysql.connector


# database connection
connection_object = mysql.connector.connect(host='localhost', user='root', passwd='', database='lush')
cursor_object = connection_object.cursor()

pygame.init()
screen = pygame.display.set_mode([700, 500])
caption = pygame.display.set_caption('Lush')

# speed
obstacle_speed = 4
player_speed = 4

# fonts
font_s24 = pygame.font.Font(None, 24)
font_s40 = pygame.font.Font('graphics/Malkor-Bold.ttf', 40)
font_s72 = pygame.font.Font('graphics/Malkor-Bold.ttf', 72)

# high score
highscore_record = 'Last high score : '
new_highscore_created = 'NEW HIGH SCORE CREATED!'
recordX = 200
recordY = 275
high_score = 0
highscore_creator = ''
scoreboard_lst = []
lst_tables = []

# Music and other sound effects
background_sound = mixer.Sound('graphics/Game-music.wav')
gameover_sound = mixer.Sound('graphics/Game over sound.wav')

# instructions
instructions_str1 = 'Press S to start'
instructions_str2 = 'Press SPACE BAR to jump over obstacles'
instructions_str3 = 'AVOID'
instructions_str4 = 'COLLECT                   for Bonus'
instructions_str5 = 'Press R to replay'
instructionsX = 50
instructionY1 = 150
instructionY2 = 200
instructionY3 = 250
instructionY4 = 300
instructionX5 = 550
instructionY5 = 400
instruction1Img = pygame.transform.scale(pygame.image.load('graphics/AVOID instruction.png'), (200, 65))
instruction1_imageX = 115
instruction1_imageY = 225
instruction2Img = pygame.transform.scale(pygame.image.load('graphics/COLLECT instructions.png'), (20, 20))
instruction2_imageX = 150
instruction2_imageY = 295
        
# static background
static_background_1Img = pygame.image.load('graphics/blue background final.jpg')
static_background_1X = 0
static_background_1Y = 0
static_background_1X_change = 0
static_background_1_state = 'static'
overall_background_state = 'static'

# user entry
text_box = pygame.Rect(100, 150, 500, 200)    
input_area = pygame.Rect(250, 200, 325, 40)
cont_as_guest_button = pygame.Rect(125, 275, 150, 40)
go_button = pygame.Rect(475, 275, 100, 40)
user_text = ''
active_typing = True
input_taking = True

# player
playerImg = pygame.image.load('graphics/Main Character.png')
playerX = 0
playerY = 350
playerX_change = 0
playerY_change = 0


# coin count
coin_count = 0
coin_count_textX = 500
coin_count_textY = 10

# score
score_val = 0
score_textX = 10
score_textY = 10
display_score = 0

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

# obstacle list
obstacle1path = 'graphics/Red obstacle 64 pixels.png'
obstacle2path = 'graphics/Purple obstacle.png'
obstacle3path = 'graphics/Barrel obstacle.png'
obstacle4path = 'graphics/Fire obstacle.png'
obstacle_dic = {obstacle1path: [350], obstacle2path: [350], obstacle3path: [325], obstacle4path: [375]}
obstacle_list = [obstacle1path, obstacle2path, obstacle3path, obstacle4path, obstacle1path, obstacle2path, obstacle3path, obstacle4path]
random.shuffle(obstacle_list)

# obstacle 1
obs1 = random.choice(obstacle_list)
obstacle_list.remove(obs1)
obs1Img = pygame.image.load(obs1)
obs1X = random.randrange(725,750)
obs1Y = obstacle_dic[obs1][0]
obs1X_change = -1 * obstacle_speed
obs1_state = 'static'

# obstacle 2
obs2 = random.choice(obstacle_list)
obstacle_list.remove(obs2)
obs2Img = pygame.image.load(obs2)
obs2X = random.randrange(925,950)
obs2Y = obstacle_dic[obs2][0]
obs2X_change = -1 * obstacle_speed
obs2_state = 'static'


# bonus coins
coinImg = pygame.image.load('graphics/coin.png')
coinX = random.randrange(1000, 2000)
coinY = random.randrange(250, 380)
coinX_change = -1 * obstacle_speed
coin_state = 'static'

## database stuff ##
def scoreboard_update():
    global cursor_object, connection_object, scoreboard_lst, lst_tables

    try:
        cursor_object.execute('show tables;')
        for i in cursor_object.fetchall():
            lst_tables.append(i[0])
        lst_tables.remove('guest')
        lst_tables.remove('scoreboard')
        for i in lst_tables:
            try:
                query = 'select * from '+i+' order by score desc, date desc, time desc;'
                cursor_object.execute(query)
                data = cursor_object.fetchall()
                l = [data[0][1], i]
                if l not in scoreboard_lst:
                    scoreboard_lst.append(l)
                else:
                    scoreboard_lst[scoreboard_lst.index(l)][0] = data[0][1]
            except:
                connection_object.rollback()
    except:
        connection_object.rollback()

def adding_data(username):
    global connection_object, cursor_object, display_score, high_score, run, lst_tables

    current_date_time = datetime.now()
    current_date = str(current_date_time)[0:10]
    current_time = current_date_time.strftime('%H:%M:%S')
    try:
        if username != 'guest':
            if username in lst_tables:
                try:
                    query = 'select distinct id from ' + str(username) + ';'
                    cursor_object.execute(query)
                    id = cursor_object.fetchone()[0]
                    query = "insert into " + str(username) + " values(" + str(id) + "," + str(display_score) + ",'" + str(current_date) + "','" + str(current_time) + "');" 
                    cursor_object.execute(query)
                    connection_object.commit()
                except:
                    connection_object.rollback()
            else:
                try:
                    query = 'create table '+username+'(ID integer, SCORE integer, DATE date, TIME time, unique(date,time));'
                    cursor_object.execute(query)
                    connection_object.commit()
                    new_id = len(lst_tables) + 2
                    query = "insert into " + str(username) + " values(" + str(new_id) + "," + str(display_score) + ",'" + str(current_date) + "','" + str(current_time) + "');"
                    cursor_object.execute(query)
                    connection_object.commit()
                except:
                    connection_object.rollback()
        else:
            try:
                query = "insert into guest values(1, "+str(display_score)+", '"+str(current_date)+"', '"+str(current_time)+"');"
                cursor_object.execute(query)
                connection_object.commit()
            except:
                connection_object.rollback()

    except:
        connection_object.rollback()

def user_entry():
    global user_text

    user_text_surface = font_s24.render(user_text, True, (0, 0, 0))
    name_text = font_s24.render('Username: ', True, ((0, 0, 0)))
    button_text1 = font_s24.render('Cont. as Guest', True, (0, 0, 0))
    button_text2 = font_s24.render('Enter', True, (0, 0, 0))
    pygame.draw.rect(screen, pygame.Color(0, 0 ,0), text_box, 2, 5)
    pygame.draw.rect(screen, pygame.Color(249, 249, 224), cont_as_guest_button, border_radius = 10)
    pygame.draw.rect(screen, pygame.Color(249, 249, 224), go_button, border_radius = 10)
    pygame.draw.rect(screen, pygame.Color(249, 249, 224), input_area, border_radius = 10)
    screen.blit(name_text, (125, 215))
    screen.blit(user_text_surface, (265, 215))
    screen.blit(button_text1, (140, 290))
    screen.blit(button_text2, (505, 290))

def show_highscore(x, y):
    if display_score < high_score:
        highscore = font_s24.render(highscore_record + str(high_score), True, (225,225,225))
        screen.blit(highscore, (x, y))
    else:
        highscore = font_s24.render(new_highscore_created, True, (225, 225, 225))
        screen.blit(highscore, (x, y))

def instruction1(x, y):
    ins1 = font_s24.render(instructions_str1, True, (225, 225, 225))
    screen.blit(ins1, (x, y))

def instruction2(x, y):
    ins2 = font_s24.render(instructions_str2, True, (225, 225, 225))
    screen.blit(ins2, (x, y))

def instruction3(x, y):
    ins3 = font_s24.render(instructions_str3, True, (225, 225, 225))
    screen.blit(ins3, (x, y))

def instruction4(x, y):
    ins4 = font_s24.render(instructions_str4, True, (225, 225, 225))
    screen.blit(ins4, (x, y))

def instruction5(x, y):
    ins5 = font_s24.render(instructions_str5, True, (225, 225, 225))
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
    global display_score
    display_score = (score_val+(coin_count*2500))//250
    score = font_s40.render('Score: '+ str(display_score), True, (225,225,225))
    screen.blit(score, (x, y))

def show_coins(x, y):
    coincounter = font_s40.render('Coins: '+ str(coin_count), True, (225,225,225))
    screen.blit(coincounter, (x, y))

def coins_collected(x, y):
    collectedcoins = font_s40.render('Coins: '+ str(coin_count), True, (225,225,225))
    screen.blit(collectedcoins(x,y))

def gameover_display(x, y):
    end_txt = font_s72.render('G A M E   O V E R !', True, (225, 225, 225))
    screen.blit(end_txt, (x, y))

def obstacle1(x, y):
    global obs1_state
    obs1_state = 'moving'
    screen.blit(obs1Img, (x, y))

def obstacle2(x, y):
    global obs2_state
    obs2_state = 'moving'
    screen.blit(obs2Img, (x, y))

def iscollision1(playerX, playerY, obs1X, obs1Y):
    distance1 = math.sqrt(math.pow(playerX - obs1X, 2) + math.pow(playerY - obs1Y, 2))
    if distance1 < 30:
        return True
    else:
        return False

def iscollision2(playerX, playerY, obs2X, obs2Y):
    distance2 = math.sqrt(math.pow(playerX - obs2X, 2) + math.pow(playerY - obs2Y, 2))
    if distance2 < 30:
        return True
    else:
        return False

def coin(x, y):
    global coin_state
    coin_state = 'moving'
    screen.blit(coinImg, (x, y))

def isbonus(playerX, playerY, coinX, coinY):
    global coin_count
    distance_coin = math.sqrt(math.pow(playerX - coinX, 2) + math.pow(playerY - coinY, 2))
    if distance_coin < 35:
        return True 
    else:
        return False

def var_initialisation():
    global static_background_1Img, static_background_1X, static_background_1Y, static_background_1X_change, static_background_1_state, overall_background_state, playerImg, playerX, playerY, playerX_change, playerY_change, score_val, font_s40, font_s72, gameover_textX, gameover_textY, gameover, gameover_sound_stop, obstacle_dic, obstacle_list, obs1, obs1Img, obs1X, obs1Y, obs1X_change, obs1_state, obs2, obs2Img, obs2X, obs2Y, obs2X_change, obs2_state, coinX, coinY, coinX_change, coin_state, coin_count, display_score

    static_background_1Img = pygame.image.load('graphics/blue background final.jpg')
    static_background_1X = 0
    static_background_1Y = 0
    static_background_1X_change = 0
    static_background_1_state = 'static'
    overall_background_state = 'static'
    playerImg = pygame.image.load('graphics/Main Character.png')
    playerX = 0
    playerY = 350
    playerX_change = 0
    playerY_change = 0
    score_val = 0
    display_score = 0
    font_s40 = pygame.font.Font('graphics/Malkor-Bold.ttf', 40)
    font_s72 = pygame.font.Font('graphics/Malkor-Bold.ttf', 72)
    gameover_textX = 100
    gameover_textY = 200
    gameover = False
    gameover_sound_stop = False

    obstacle_dic = {obstacle1path: [350], obstacle2path: [350], obstacle3path: [325], obstacle4path: [375]}
    obstacle_list = [obstacle1path, obstacle2path, obstacle3path, obstacle4path, obstacle1path, obstacle2path, obstacle3path, obstacle4path]
    random.shuffle(obstacle_list)
    obs1 = random.choice(obstacle_list)
    obstacle_list.remove(obs1)
    obs1Img = pygame.image.load(obs1)
    obs1X = random.randrange(725,750)
    obs1Y = obstacle_dic[obs1][0]
    obs1X_change = -1 * obstacle_speed
    obs1_state = 'static'
    obs2 = random.choice(obstacle_list)
    obstacle_list.remove(obs2)
    obs2Img = pygame.image.load(obs2)
    obs2X = random.randrange(925,950)
    obs2Y = obstacle_dic[obs2][0]
    obs2X_change = -1 * obstacle_speed
    obs2_state = 'static'

    coinX = random.randrange(1000, 2000)
    coinY = random.randrange(250, 380)
    coinX_change = -1 * obstacle_speed
    coin_state = 'moving'
    coin_count = 0

scoreboard_update()
run = True
while run:
    if gameover:
        background_sound.stop()
        playerX_change = 0
        playerY_change = 0
        static_background_1X_change = 0
        obs1X_change = 0
        obs2X_change = 0
        overall_background_state = 'static'
        coinX_change = 0
        adding_data(user_text.lower())

        if gameover_sound_stop == False:
            gameover_sound.play()
            gameover_sound_stop = True
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_area.collidepoint(event.pos):
                active_typing = True
            elif cont_as_guest_button.collidepoint(event.pos):
                user_text = 'guest'
                active_typing = False
                input_taking = False
            elif go_button.collidepoint(event.pos):
                active_typing = False
                input_taking = False
            else:
                active_typing = False
        
        if event.type == pygame.KEYUP and not input_taking:
            if event.key == pygame.K_r:
                gameover = False
                overall_background_state = 'moving'
                playerX_change = player_speed
                static_background_1X_change = 0.5
                user_entry()
                if overall_background_state == 'moving':
                    if event.key == pygame.K_SPACE:
                        if playerY >= 350:
                            playerY_change = -3
                var_initialisation()
        
        if event.type == pygame.KEYDOWN and active_typing:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:len(user_text)-1]
            else:
                user_text += event.unicode

        if event.type == pygame.KEYDOWN and not input_taking:
            if event.key == pygame.K_s:
                overall_background_state = 'moving'
                playerX_change = player_speed
                static_background_1X_change = 0.5
            if overall_background_state == 'moving':
                if event.key == pygame.K_SPACE:
                    if playerY >= 350:
                        playerY_change = -3

    if not gameover:
        gameover_sound.stop()
        background_sound.play()
        if playerY < 250:
            playerY_change = 3
        if playerY > 350:
            playerY = 350
        if playerX > 225:
            playerX_change = 0

            # obstacle movements
            # obstacle 1
            if obs1X <= -65:
                obs1X = random.randrange(725, 750)
                obs1_state = 'static'
            if obs1_state == 'moving':
                obstacle1(obs1X, obs1Y)
                obs1X += obs1X_change
            # obstacle 2
            if obs2X <= -65:
                obs2X = random.randrange(925, 950)
                obs2_state = 'static'
            if obs2_state == 'moving':
                obstacle2(obs2X, obs2Y)
                obs2X += obs2X_change
            if -75 < obs1X - obs2X < 75:
                obs2X += 100
            # coin movement
            if coinX <= -20:
                coinX = random.randrange(1000, 2000)
                coinY = random.randrange(250, 380)
                coin_state = 'static'
            if coin_state == 'moving':
                coin(coinX, coinY)
                coinX += coinX_change

        # background movement
        if overall_background_state == 'moving':
            static_background_1X -= static_background_1X_change
            score_val += 1

        if static_background_1X < -14000:
            static_background_1X = 0
        
        # bonus
        bonus = isbonus(playerX, playerY, coinX, coinY)
        if bonus:
            coin_count += 1
            coinX = random.randrange(1000, 2000)
            coinY = random.randrange(250, 380)

    # Collisions
    collision1 = iscollision1(playerX, playerY, obs1X, obs1Y)
    collision2 = iscollision2(playerX, playerY, obs2X, obs2Y)
    gameover = collision1 or collision2

    playerX += playerX_change
    playerY += playerY_change

    static_background_1(static_background_1X, static_background_1Y)
    show_score(score_textX, score_textY)
    show_coins(coin_count_textX, coin_count_textY)
    coin(coinX, coinY)
    obstacle1(obs1X, obs1Y)
    obstacle2(obs2X, obs2Y)
    player(playerX, playerY)

    # Display Part
    if gameover:
        show_highscore(recordX, recordY)
        show_score(score_textX, score_textY)
        show_coins(coin_count_textX, coin_count_textY)
        gameover_display(gameover_textX, gameover_textY)
        instruction5(instructionX5, instructionY5)
        mixer.music.stop()
    if overall_background_state == 'static' and not gameover and not active_typing and not input_taking:
        instruction1(instructionsX, instructionY1)
        instruction2(instructionsX, instructionY2)
        instruction3(instructionsX, instructionY3)
        instruction4(instructionsX, instructionY4)
        instruction_image1(instruction1_imageX, instruction1_imageY)
        instruction_image2(instruction2_imageX, instruction2_imageY)
    if input_taking:
        user_entry()
    pygame.display.update()
scoreboard_update()
scoreboard_update()
print('-'*9,'LEADERBOARD','-'*9)
print('| RANK | USERNAME | HIGHSCORE |')
for i in range(len(scoreboard_lst)):
    print('|  ',i+1,' |  ', scoreboard_lst[i][1],'  |   ', scoreboard_lst[i][0],'    |')
connection_object.close()
