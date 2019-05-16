
#
import pygame, random
from pygame.locals import *

FPS = 15
width = 640
height = 480
cellsize = 20
assert width % cellsize == 0
assert height % cellsize == 0
cellwidth = int(width / cellsize)
cellheight = int(height / cellsize)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 102, 255)
green = (0, 128, 255)
darkgray = (0, 150, 100)
background = black
head = 0
clock = pygame.time.Clock()
introduction = True
count = 0


def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score = " + str(score), 1, white)
    screen.blit(text, (x, y))


def main():
    global screen
    global clock
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("wormy!")
    showStartScreen()

    while True:
        return runGame()




def foodlocation():
    return {"x": random.randint(0, cellwidth - 2), "y": random.randint(0, cellheight - 2)}


def runGame():
    global count
    direction = "right"

    startx = random.randint(5, cellwidth - 6)
    starty = random.randint(6, cellheight - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty},
                  {'x': startx - 3, 'y': starty},
                  {'x': startx - 4, 'y': starty}
                  ]

    food = foodlocation()

    while True:
        draw_score(screen, width/2, height/2, count)
        if count > 16:
            return 0
        for event in pygame.event.get():
            if event.type == QUIT:
                return 1

            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction = "left"
                elif event.key == K_RIGHT:
                    direction = "right"
                elif event.key == K_UP:
                    direction = "up"
                elif event.key == K_DOWN:
                    direction = "down"

        if wormCoords[head]['x'] == -1:
            wormCoords[head]['x'] = cellwidth

        elif wormCoords[head]['x'] == cellwidth:
            wormCoords[head]['x'] = -1

        elif wormCoords[head]['y'] == cellheight:
            wormCoords[head]['y'] = -1

        elif wormCoords[head]['y'] == -1:
            wormCoords[head]['y'] = cellheight

        # check apple and collision

        if wormCoords[0]["x"] == food["x"] and wormCoords[0]["y"] == food["y"]:
            count += 1
            food = foodlocation()

            length = len(wormCoords) - 1
            newtail = {"x": wormCoords[length]['x'], "y": wormCoords[length]["y"]}
            wormCoords.insert(length, newtail)

        # checkgameover
        for body in wormCoords[1:]:
            if body["x"] == wormCoords[0]["x"] and body["y"] == wormCoords[0]["y"]:
                return 1


        if direction == "up":
            newHead = {"x": wormCoords[0]['x'], "y": wormCoords[0]["y"] - 1}
        elif direction == "right":
            newHead = {"x": wormCoords[0]['x'] + 1, "y": wormCoords[0]["y"]}

        elif direction == "down":
            newHead = {"x": wormCoords[0]['x'], "y": wormCoords[0]["y"] + 1}
        elif direction == "left":
            newHead = {"x": wormCoords[0]['x'] - 1, "y": wormCoords[0]["y"]}

        wormCoords.insert(0, newHead)
        wormCoords.pop()
        screen.fill(black)
        draw_score(screen, 10, 10, count)
        drawWorm(wormCoords)
        drawfood(food)
        pygame.display.update()
        draw_score(screen, 10, 10, count)

        clock.tick(FPS)



def drawfood(coord):
    x = coord["x"] * cellsize
    y = coord["y"] * cellsize
    foodrect = pygame.Rect(x, y, cellsize, cellsize)
    pygame.draw.rect(screen, red, foodrect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * cellsize
        y = coord['y'] * cellsize
        wormrect = pygame.Rect(x, y, cellsize, cellsize)
        pygame.draw.rect(screen, green, wormrect)
        worminnerrect = pygame.Rect(x + 3, y + 3, cellsize - 9, cellsize - 9)
        pygame.draw.rect(screen, green, worminnerrect)


def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                return True


def showStartScreen():
    titleFont = pygame.font.Font("freesansbold.ttf", 50)
    font1 = titleFont.render("Wormy!", True, white, darkgray)
    myfont = pygame.font.SysFont('freesansbold.ttf', 30)
    degree1 = 0
    textsurface = myfont.render('This is the normal snake game. Press enter to start', False, white)
    textsurface2 = myfont.render('You need to get at least 17 points to win', False, white)
    while True:
        screen.fill(background)
        rotatefont1 = pygame.transform.rotate(font1, degree1)
        rotateRect1 = rotatefont1.get_rect()
        screen.blit(textsurface, (80, height-100))
        screen.blit(textsurface2, (100, height - 50))

        rotateRect1.center = (width / 2, 200)
        screen.blit(rotatefont1, rotateRect1)
        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        clock.tick(FPS)
        degree1 += 3


def quit():
    pygame.quit()




