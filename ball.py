import pygame
import random
import json
from chat_utils import *


def start_up_screen():
    clock = pygame.time.Clock()
    width = 650
    height = 580

    size = [width, height]
    start_image = pygame.image.load("instruction/falling_ball_ins.jpg")

    screen = pygame.display.set_mode(size)
    while True:
        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()

        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break



def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score = " + str(score), 1, (255,255,255))
    screen.blit(text, (x, y))


def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, (255,255,255))  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        width = 650

        self.images = []
        self.images.append(pygame.image.load('image/ball_1.png'))
        self.images.append(pygame.image.load('image/ball_2.png'))
        self.images.append(pygame.image.load('image/ball_2.png'))
        self.images.append(pygame.image.load('image/ball_4.png'))
        self.images.append(pygame.image.load('image/ball_5.png'))
        self.images.append(pygame.image.load('image/ball_6.png'))
        self.images.append(pygame.image.load('image/ball_7.png'))
        self.index = 0
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.rect.x = width/2
        self.rect.y = 100

    def update(self):
        width = 650
        height = 580
        self.index += 1

        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        self.change_y = 5
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        if self.rect.y >= width - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = height - self.rect.height
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > width:
            self.rect.x = width-50



    def go_left(self):
        self.change_x = -8

    def go_right(self):
        self.change_x = 8

    def stop(self):
        self.change_x = 0



class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height,x):
        super().__init__()
        gray = (180, 180, 180)

        self.image = pygame.Surface([width,height])
        self.r = width
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 580

        self.change_y = 0

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()



def send_result(to_sock, result, game_num, counter):
    if result == 0:
        point = game_num
    else:
        point = 0
    mysend(to_sock,
           json.dumps({"action": "gaming", "game_num": game_num, "result": result, "point": point, "counter": counter}))


def main():
    result = 5
    score = 0
    width = 650
    height = 580

    black = (0, 0, 0)
    PLAY_TIME = 30
    size = [width, height]
    screen = pygame.display.set_mode(size)
    WHITE = (255, 255, 255)
    pygame.init()
    background_image = pygame.image.load("image/fall_ball_background.png")

    clock = pygame.time.Clock()
    speed = 5
    start_up_screen()
    score = 0
    global win
    start_time = pygame.time.get_ticks()
    pygame.display.set_caption("Falling_ball")
    done = False
    block_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()
    check_num_list = pygame.sprite.Group()

    for i in range(2):
        width1 = random.randint(50, 100)
        height1 = 10

        block = Platform(width1,height1,width/2)
        block_list.add(block)
        check_num_list.add(block)

    player = Player()
    player.update()
    player_list.add(player)


    while not done:


        if player.rect.y > height or player.rect.y < -5:
            # result = 1
            # send_result()
            return 1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # result = 1
                # send_result(to_sock, result, game_num, counter)
                return 1


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                if event.key == pygame.K_RIGHT:
                    player.stop()


        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)
        draw_timer(screen, 50, 450, time_left)

        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            # result = 0
            # send_result(to_sock, result, game_num, counter)
            return 0



        for i in check_num_list:
            if i.rect.y < height/2:
                check_num_list.remove(i)

        if len(check_num_list) < 2:
            width1 = random.randint(100, 200)
            height1 = random.randint(10, 40)
            block1 = Platform(width1, height1, random.randint(350, width))
            block2 = Platform(width1, height1, random.randint(0, 350))
            check_num_list.add(block1)
            check_num_list.add(block2)
            block_list.add(block1)
            block_list.add(block2)

        block_list.update()
        collide_list = pygame.sprite.spritecollide(player, block_list, False)
        if len(collide_list) != 0:
            player.rect.bottom -= speed+1
            player.rect.y -= speed+1

        player_list.update()
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # result = 1
                # send_result(to_sock, result, game_num, counter)
                return 1


        draw_timer(screen, 50, 50, time_left)
        draw_score(screen, 70, 10, score)
        score += 1

        player_list.draw(screen)
        block_list.draw(screen)
        clock.tick(60)

        pygame.display.update()




    pygame.quit()


def quit():
    pygame.quit()




