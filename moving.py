
import pygame
import random

def start_up_screen():
    SIZE = WIDTH, HEIGHT = 900, 700
    BACKGROUND_COLOR = pygame.Color('black')
    FPS = 40
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    start_image = pygame.image.load("instruction/hunter.png")
    while True:
        screen.blit(start_image, (0, 0))
        clock.tick(60)
        pygame.display.update()
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break


def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, (255,255,255))  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen

def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score = " + str(score), 1, (255,255,255))
    screen.blit(text, (x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.images = []
        self.images.append(pygame.image.load('image/walk1.png'))
        self.images.append(pygame.image.load('image/walk2.png'))
        self.images.append(pygame.image.load('image/walk3.png'))
        self.images.append(pygame.image.load('image/walk4.png'))
        self.images.append(pygame.image.load('image/walk5.png'))
        self.images.append(pygame.image.load('image/walk6.png'))


        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.index += 1
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

    def go_left(self):
        self.change_x = -10

    def go_right(self):
        self.change_x = 10

    def go_up(self):
        self.change_y = -10

    def go_down(self):
        self.change_y = 10


    def stop(self):
        self.change_x = 0
        self.change_y = 0


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        WIDTH, HEIGHT = 900, 700
        self.images = []
        self.images.append(pygame.image.load('image/star.png'))
        self.images.append(pygame.image.load('image/star2.png'))
        self.images.append(pygame.image.load('image/star.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]



class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super(Coin, self).__init__()
        SIZE = WIDTH, HEIGHT = 900, 700
        self.images = []
        self.images.append(pygame.image.load('image/gold_1.png'))
        self.images.append(pygame.image.load('image/gold_2.png'))
        self.images.append(pygame.image.load('image/gold_3.png'))
        self.images.append(pygame.image.load('image/gold_4.png'))
        self.images.append(pygame.image.load('image/gold_5.png'))
        self.images.append(pygame.image.load('image/gold_6.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,WIDTH)
        self.rect.y = random.randint(0, HEIGHT)


    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

def main():
    PLAY_TIME = 40

    SIZE = WIDTH, HEIGHT = 900, 700
    BACKGROUND_COLOR = pygame.Color('black')
    FPS = 40
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    start_up_screen()
    score = 0
    pygame.init()
    start_time = pygame.time.get_ticks()

    player = Player()
    coin_list = pygame.sprite.Group()
    star_list = pygame.sprite.Group()
    for i in range(0, 40):
        coin = Coin()
        coin_list.add(coin)
    player_list = pygame.sprite.Group(player)



    while True:
        if score == 300:
            return 0
        hit_list = pygame.sprite.spritecollide(player, coin_list, True)
        if len(hit_list)!=0:
            score += 10*len(hit_list)
        hi_list = pygame.sprite.spritecollide(player, star_list, True)
        if len(hi_list)!=0:
            score += 10*len(hi_list)
        time_left = pygame.time.get_ticks() - start_time
        time_left = time_left / 1000
        time_left = PLAY_TIME - time_left
        time_left = int(time_left)
        draw_timer(screen, 50, 450, time_left)

        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            return 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.go_up()
                if event.key == pygame.K_DOWN:
                    player.go_down()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.stop()
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.stop()

        draw_timer(screen, 50, 50, time_left)
        player_list.update()
        coin_list.update()
        star_list.update()
        screen.fill(BACKGROUND_COLOR)

        player_list.draw(screen)
        draw_score(screen, 100, 100, score)
        coin_list.draw(screen)
        star_list.draw(screen)
        draw_timer(screen, 50, 50, time_left)
        pygame.display.update()

        clock.tick(50)
        if (time_left < 20):
            for i in coin_list:
                coin_list.remove(i)

        if time_left == 18:
            for i in range(0, 1):
                star = Star()
                star_list.add(star)

def quit():
    pygame.quit()


