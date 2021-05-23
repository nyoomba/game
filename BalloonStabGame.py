### Stabby balloon game
import random

import pygame
import time
import sqlite3
import pandas as pd

# external function passes name
name = "ames"

#################################################################

## First get the sad data from the SQLite database

# connect to the database
conn = sqlite3.connect('sql/testNyoomba.db')

print("Opened database successfully")

# Query for sad
query = "SELECT rowID, SadScale, upsetTitle FROM upset WHERE userName = '" + name + "'"

result = conn.execute(query)

#number of balloons spawned
balloons = 5
data_found = False

# check if queryset is empty (if it is just use ranodom balloons)
if result.rowcount == 0:
    print ("data not found")

else:
    balloons = result.rowcount
    data_found = True

    df = pd.DataFrame()

    for row in result:
        # print("ID = ", row[0])
        # print("SADSCALE = ", row[1])
        # print("UPSETTITLE = ", row[2])
        # print("\n")

        new_row = {'dbId': row[0], 'sadscale': int(row[1]), 'upsettitle': row[2]}

        # append row to the dataframe
        df = df.append(new_row, ignore_index=True)

    print(df)
    print ("data retrieved \n")

# close SQLite connection
conn.close()

########################################################

## Pygame segment
# start pygame
pygame.init()

# display window size
display_width = 800
display_height = 600

balloon_speed = 5

# set colour values arrrays
black = (0, 0, 0)
white = (255, 255, 255)
red = (240, 91, 74)
green = (89, 240, 86)
blue = (47, 235, 245)

# width of icon
stabby_width = 135
stabby_height = 154

# create display window
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('nyoomba')

# create clock timer
clock = pygame.time.Clock()

#load images
stabbyImg = pygame.image.load('otherSources/glow_nyoomba_stabby.png')
gladBotImg = pygame.image.load('otherSources/glow_nyoomba_gladbot.png')
# print(stabbyImg.get_rect().size)
stabbyImg = pygame.transform.scale(stabbyImg, (stabby_width, stabby_height))

# set program icon
programIcon = pygame.image.load('otherSources/logo.png')
pygame.display.set_icon(programIcon)

# render stabby at the start of the game
def stabby(x, y):
    # render stabby in the game using blit
    gameDisplay.blit(stabbyImg, (x, y))

def gladBot(x, y):
    # render stabby in the game using blit
    gameDisplay.blit(gladBotImg, (x, y))

def text_objects(text, font):
    # render text objects
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def balloon(balloon_radius, balloon_x, balloon_y, color, title):
    balloon_body = pygame.draw.circle(gameDisplay, color, (balloon_x, balloon_y), balloon_radius)

    text_font = pygame.font.Font('freesansbold.ttf', 20)
    text_obj = text_font.render(title, True, black)
    text_rect = text_obj.get_rect()
    text_rect.center = (balloon_x, balloon_y)

    gameDisplay.blit(text_obj, text_rect)

def display_win():
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("You did it!", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    x = (display_width * 0.425)
    y = (display_height * 0.75)
    gladBot(x, y)

    pygame.display.update()

    time.sleep(2)


def game_loop():

    x = (display_width * 0.425)
    y = (display_height * 0.75)

    x_change = 0
    pos_shift_left = False
    pos_shift_right = False

    balloon_x = 0
    balloon_y = 0

    count = 0
    balloon_text = ""

    obj_exists = False


    win = False

    gameExit = False

    pop_sound = pygame.mixer.Sound("otherSources/pop.wav")
    win_sound = pygame.mixer.Sound("otherSources/Pickup_Coin4.wav")

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    pos_shift_left = True

                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    pos_shift_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0


        if not pos_shift_left and (x > display_width - stabby_width):
            x_change = 0
        elif not pos_shift_right and x < 0:
            x_change = 0
        else:
            x += x_change

        pos_shift_left = False
        pos_shift_right = False


        if df.shape[0] != 0:

            if not obj_exists:
                # create new shape with text

                # get position
                balloon_y = 100
                # randrange gives you an integral value
                balloon_x = random.randint(100, display_width - 100)

                obj_exists = True

                # get text to display
                row_1 = df.sample()
                current_text_id = row_1.iloc[0]["dbId"]
                balloon_text = row_1.iloc[0]["upsettitle"]
                balloon_color = random.choice([blue, red, green])

                obj_exists = True
            else:
                balloon_y += balloon_speed
                if balloon_y + 80 > display_width:
                    obj_exists = False

        else:
            win = True
            # balloon_y = display_height + 90
            x = (display_width * 0.425)
            y = (display_height * 0.75)
            gameDisplay.fill(white)
            pygame.mixer.Sound.play(win_sound)
            display_win()
            # time.sleep(2)
            gameExit = True


        if balloon_x > x - 80 and balloon_x < x + 240 and balloon_y > y - 80 and balloon_y < y + 80:
            # balloon pop
            indexNames = df[df['dbId'] == current_text_id].index
            df.drop(indexNames, inplace=True)
            # print(df)
            pygame.mixer.Sound.play(pop_sound)
            obj_exists = False

        gameDisplay.fill(white)

        if obj_exists:
            balloon(80, balloon_x, balloon_y, balloon_color, balloon_text)
        if not win:
            stabby(x, y)


        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()

# no need to quit
quit()