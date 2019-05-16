import pygame
from pygame.locals import *
import random

pointcounter = 0
screensize = (700,700)
background_image = pygame.image.load("image/blue.png")
start_image = pygame.image.load("instruction/bouncing_ball_ins.png")
PLAY_TIME = 30
WHITE = (255,255,255)

clock = pygame.time.Clock()

def start_up_screen():
    while True:
        pygame.init()
        screen = pygame.display.set_mode(screensize)
        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break


def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, WHITE)  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen


class Pong(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.centerx = 0
        self.centery = int(screensize[1]*0.5)
        self.image = pygame.image.load("image/bouncing_ball.png")
        self.rect = self.image.get_rect()
        self.color = (10,150,100)
        self.direction = [1,1]
        self.speedx = 9
        self.speedy = 9
        self.hit_edge_left = False
        self.hit_edge_right = False


    def update(self, player_paddle, ai_paddle):


        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= 700-1:
            self.direction[1] = -1

        if self.rect.right >= 700-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1

        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1


class AIPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = 7
        self.centery = int(screensize[1]*0.5)

        self.height = 130
        self.width = 20

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (random.randint(1,255),random.randint(1,255),random.randint(1,255))
        self.speed = 10

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize
        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 15
        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))

        self.speed = 10
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


def main():

    start_up_screen()

    pygame.init()
    screen = pygame.display.set_mode(screensize)

    screen.blit(background_image, (-20, -10))

    pong = Pong()
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)
    start_time = pygame.time.get_ticks()

    running = True
    ball_list = pygame.sprite.Group()
    ball_list.add(pong)

    while running:

        clock.tick(100)

        for event in pygame.event.get():
            if event.type == QUIT:
                return 1

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0


        ai_paddle.update(pong)

        player_paddle.update()

        ball_list.update(player_paddle,ai_paddle)

        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)
        draw_timer(screen, 50, 450, time_left)

        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            return 0

        if pong.hit_edge_right:
            return 1

        screen.blit(background_image, (-25, -10))

        ai_paddle.render(screen)
        player_paddle.render(screen)
        ball_list.draw(screen)
        draw_timer(screen, 50, 50, time_left)

        pygame.display.update()
    pygame.quit()



def quit():
    pygame.quit()

#
# a = main()
# print(a)

